#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Pyro4

search = Pyro4.Proxy( "PYRONAME:crawling" )

with open( "SearchResult.txt", "w" ) as handle:
    handle.write( search.crawl_web( "https://tunein.com", 2 ) )
handle.close()

print ('Operation completed successfully!')
