import scrapy

class MoodContemplativeSpiderSpider(scrapy.Spider):
    name = "mood_contemplative_spider"
    allowed_domains = ["songsara.net"]
    start_urls = ["https://songsara.net/mood/contemplative"]

    def parse(self, response):
        # get all albums
        albums = response.css("section.posting")

        # process on data received
        for album in albums:
            relative_url = album.css("div.post-img-hover a::attr(href)").get()
            if relative_url is not None:
                yield response.follow(relative_url, callback=self.parse_song)

        next_page_element = response.css("a.nextpostslink::attr(href)").get()
        if next_page_element is not None:
            yield response.follow(next_page_element, callback=self.parse)

    def parse_song(self, response):
        # get more information about song
        song = response.css("article.postbox-single")
        
        # Extract image URL from the first selector
        image_url = song.css("img.attachment-pic-single::attr(src)").get()
        
        # Extract all songs url
        songs_url = song.xpath("//ul[@class='audioplayer-audios']/li/@data-src").extract()
        
        # Check if the image URL is invalid and use the fallback selector if needed
        if image_url and image_url.startswith("data:"):
            image_url = song.css("figure.pic-s img.attachment-pic-single::attr(data-lazy-src)").get()

        # clone data
        yield {
            "url": response.url,
            "image": image_url,
            "title": song.css("h2.AL-Si::text").get(),
            "artist": song.css("div.AR-Si a::text").get(),
            "songs": songs_url,
        }
