# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 21:38:54 2018

@author: Lourenço Neto
"""

import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "brickset_spider"
    start_urls = ['http://brickset.com/sets/year-2016']