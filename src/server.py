#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import Pyro4

@Pyro4.behavior( instance_mode = "percall" )
class Crawler( object ):

    def get_page( self, url ):
        self.url = url
        try:
            with urllib.request.urlopen( self.url ) as html:
                return str( html.read() )
        except:
            return ""

    def get_next_target( self, page ):
        self.page = page
        start_link = self.page.find( '<a href=' )

        if ( start_link == -1 ):
            return None, 0

        start_quote = self.page.find( '"', start_link )
        end_quote   = self.page.find( '"', start_quote + 1 )
        url = self.page[start_quote+1:end_quote]
        return url, end_quote

    def get_all_links( self, page ):
        self.page = page
        links = []
        while True:
            url,endpos = self.get_next_target( self.page )
            if url:
                links.append( url )
                self.page = self.page[endpos:]
            else:
                break
        return links

    def union( self, p, q ):
        self.p = p
        self.q = q
        for e in self.q:
            if e not in self.p:
                self.p.append( e )

    @Pyro4.expose
    def crawl_web( self, seed, max_page ):

        self.seed = seed
        self.max_page = max_page

        tocrawl = [self.seed]
        crawled = []
        index   = []

        while tocrawl:
            page = tocrawl.pop()
            if page not in crawled and len( tocrawl ) < self.max_page:
                content_page = self.get_page( page )
                print ( self.get_page )
                self.union( tocrawl, self.get_all_links( content_page ) )
                crawled.append( page )

        return crawled


def main():

    Pyro4.Daemon.serveSimple(
        {
            Crawler: "crawling"
        },
        host = 'localhost',
        ns = True)


if __name__ == "__main__":
    main()
