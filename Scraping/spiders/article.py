# -*- coding: utf-8 -*-
import scrapy
from plazapublica_daily.items import article, articles


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['plazapublica.com.gt']
    start_urls = ['https://plazapublica.com.gt/']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'archivos//featured_article-%(time)s.json'
    }

    def parse(self, response):
        host = self.allowed_domains[0]

        for link in response.css(".views-field-title .field-content > a"):
            link = f"{link.attrib.get('href')}"
            yield response.follow(link,callback=self.parse_detail, meta={'link' : link})

    def parse_detail(self,response):
        items = articles()
        item = article()

        items["link"] = response.meta["link"]
        item["title"] =  response.css(".even > h2::text").extract()
        item["paragraph"] = response.css(".field-name-field-vineta-enserio .field-items .field-item > p::text").extract()
        
        items["body"] = item
        return items
