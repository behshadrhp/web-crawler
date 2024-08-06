import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = "best_movies"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250/"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//ul/li/div[@class='ipc-metadata-list-summary-item__c']/div/div/div/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):

        title = response.xpath("//div[@class='sc-491663c0-3 kNMkxz']/div/h1/span/text()").get()
        description = response.xpath("//section[@class='sc-1f50b7c-4 hIXNlF']/p/span[3]/text()").get()
        year_make = response.xpath("//div[@class='sc-491663c0-3 kNMkxz']/div/ul/li/a/text()").get()
        time = response.xpath("//div[@class='sc-491663c0-3 kNMkxz']/div/ul/li[3]/text()").get()
        rating = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]/text()").get()
        count_rating = response.xpath("//*[@id='__next']/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[3]/text()").get()
        
        yield {
            "url": response.url,
            "title": title,
            "description": description,
            "year_make": year_make,
            "time": time,
            "raging": rating,
            "count_rating": count_rating
        }
