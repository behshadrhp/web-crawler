from urllib.parse import unquote

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LastSeriesSpider(CrawlSpider):
    name = "last_series"
    allowed_domains = ["www.uptvs.com"]
    start_urls = ["https://www.uptvs.com/category/seriessz"]

    rules = (Rule(LinkExtractor(restrict_xpaths="//article[@class='post-layout bg-white rounded mb-20 shadow p-20']/div/div/a"), callback="parse_item", follow=True),)

    def parse_item(self, response):

        title = response.xpath("normalize-space(//div[@class='col-md col-12 text-md-right text-center']/h1/text())").get()
        episode = response.xpath("normalize-space(//div[@class='col-md col-12 text-md-right text-center']/span/text())").get()
        genre = response.xpath("normalize-space(//div[@class='post-single-meta pt-lg-half pt-md-half mt-1 pb-10 small-14']/div/div/span/a/text())").getall()
        year_make = response.xpath("normalize-space(//div[@class='row']/div[1]/text()[3])").get()
        country_make = response.xpath("normalize-space(//span[@class='d-md-inline-block d-none']/text())").get()
        time_play = response.xpath("normalize-space(//div[@class='row']/div[1]/text()[8])").get()
        age_range = response.xpath("normalize-space(//span[@class='text-yellow']/text())").get()
        imdb_rating = response.xpath("normalize-space(//span[@class='font-weight-bold text-white small-15']/text())").get()
        imdb_count_rating = response.xpath("normalize-space(//span[@class='text-gray d-lg-inline d-none small-12']/text())").get()
        story = response.xpath("normalize-space(//p[@class='show-read-more']/text())").get()

        if genre[0] == "":
            genre.pop(0)

        yield {
            "url": unquote(response.url),
            "title": title,
            "episode": episode,
            "genre": genre,
            "year make": year_make,
            "country make": country_make,
            "time play": time_play,
            "age range": age_range,
            "imdb rating": imdb_rating,
            "imdb count rating": imdb_count_rating,
            "story": story
        }
