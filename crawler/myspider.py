# -*- codin\g: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import logging


class DerimodProductCrawler(scrapy.Spider):
    name = 'derimod_product_crawler'
    start_urls = ['https://www.derimod.com.tr/kadin-tum-ayakkabilar/', 'https://www.derimod.com.tr/erkek-tum-ayakkabilar/',
                  'https://www.derimod.com.tr/kadin-deri-ceket/', 'https://www.derimod.com.tr/erkek-deri-ceket/']

    def start_requests(self):
        logging.info('Waiting for responses...')
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1.0})

    def parse(self, response):
        html = BeautifulSoup(response.text, 'html.parser')
        prod_list = html.find_all("div", attrs={
                                  "class": "col-sm-4 col-xs-6 padding-lg list-content-product-item list__content--margin"})
        logging.info('Found {} Products:'.format(len(prod_list)))
        for prod in prod_list:
            logging.info(
                "Product Uri: https://www.derimod.com.tr{}".format(prod.select('div > div.img-wrapper.js-equal-height > div > a')[0].get('href')))
            logging.info("Product Name: {}".format(prod.select(
                'div > div.product-list-bottom-content > span.product-name')[0].get_text()))
            logging.info("Product Price: {}".format(prod.select(
                'div > div.product-list-bottom-content > span.product-price.line-through')[0].get_text()))
