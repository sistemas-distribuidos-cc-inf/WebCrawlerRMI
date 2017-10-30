#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Pyro4

def main():

    search = Pyro4.Proxy( "PYRONAME:crawling" )
    print( 'Client started.\n' )

    with open( 'Search.txt', 'w' ) as handle:
        handle.write( str( search.crawl_web( "https://tunein.com", 3 ) ) )
    handle.close()

    print( 'Success...\n' )

if __name__ == "__main__":
    main()
