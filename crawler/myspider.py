# -*- codin\g: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
import logging


class LCWProductUriCrawler(scrapy.Spider):
    name = 'lcw_product_uri_crawler'

    script = """
  	function main(splash)
	  splash.private_mode_enabled = false
	  
	  local url = splash.args.url
	  assert(splash:go(url))
	  assert(splash:wait(2.0))

          local element=splash:select('#divModels > div:nth-child(6) > div.col-sm-12.col-md-10 > div.paging-process > a')
	  if element then 
	    assert(element:mouse_click()) 
	  end  

	  assert(splash:wait(2.0))

	  local prod_len = 420
	  local get_body_height = splash:jsfunc("function() {return document.body.scrollHeight;}")
	  local scroll_num = (get_body_height()/prod_len)
	  for i=1,scroll_num do
	    splash.scroll_position = {y=prod_len*i} 
      assert(splash:wait(1.0))
	  end

	  return {
	    html = splash:html(),
	  }
	end
            """
    start_urls = ["https://www.lcwaikiki.com/tr-TR/TR/etiket/kadin-cok-satanlar",
                  "https://www.lcwaikiki.com/tr-TR/TR/etiket/erkek-cok-satanlar",
                  "https://www.lcwaikiki.com/tr-TR/TR/etiket/kiz-cocuk-cok-satanlar"]

    def start_requests(self):
        logging.info('Waiting for responses...')
        for url in self.start_urls:
            yield SplashRequest(url=url.strip(), callback=self.parse, endpoint='execute',
                                args={'lua_source': self.script, 'timeout': 90})

    def parse(self, response):
        html = BeautifulSoup(response.text, 'html.parser')
        urun_list = html.find_all("a", attrs={"data-tracking-category": "UrunDetay"})
        logging.info('Found {} Products:'.format(len(urun_list)))
        for urun in urun_list:
            logging.info("Product-Uri: https://www.lcwaikiki.com/{}".format(urun["href"]))
