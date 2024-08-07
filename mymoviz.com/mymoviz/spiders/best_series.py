from typing import Iterable
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestSeriesSpider(CrawlSpider):
    name = "best_series"
    allowed_domains = ["linpink.xyz"]
    start_urls = ["https://linpink.xyz/tvshows?oB=3&limit=250&&minVotes=50000"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//article[@class='movie clearfix']/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        
        title = response.xpath("//div[@class='-title']/h1/text()").get()
        subtitle = response.xpath("//h1[@class='movie-titlep']/a/text()").get()
        year_make = response.xpath("//div[@class='-title']/h1/span/text()").get()
        age_range = response.xpath("//ul[@class='-menu2']/li/a/span/text()").get()
        time_play = response.xpath("//ul[@class='-menu2']/li[2]/text()").get()
        genre = response.xpath("//li[@class='-genre']/a/text()").getall()
        imdb_rating = response.xpath("//div[@class='-rating-rating']/text()").get()
        imdb_count_user_rating = response.xpath("//div[@class='-rating-users']/text()").get()
        description = response.xpath("//section[@class='box-movie-description']/text()").get()

        yield {
            "url": response.url,
            "title": title,
            "subtitle": subtitle,
            "year_make": year_make,
            "age_range": age_range,
            "time_play": time_play,
            "genre": genre,
            "imdb rating": imdb_rating,
            "imdb count user rating": imdb_count_user_rating,
            "description": description,
        }
