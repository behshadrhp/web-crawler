import scrapy


class MoodSpicSpiderSpider(scrapy.Spider):
    name = "mood_spic_spider"
    allowed_domains = ["songsara.net"]
    start_urls = ["https://songsara.net/mood/epic"]

    def parse(self, response):
        
        albums = response.css("article.postbox-i")
        
        for album in albums:
            
            yield{
                "url": response.url,
                "link": album.css("div.post-img-hover a::attr(href)").get(),
                "title": album.css("li.index-al::text").get(),
                "date-public": album.css("li.index-da::text").get(),
            }

        next_pages = response.css("a.nextpostslink::attr(href)").get()
        
        if next_pages is not None:
            yield response.follow(next_pages, callback=self.parse)
