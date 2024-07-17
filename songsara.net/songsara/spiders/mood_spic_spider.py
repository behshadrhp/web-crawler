import scrapy


class MoodSpicSpider(scrapy.Spider):
    name = "mood_spic_spider"
    allowed_domains = ["songsara.net"]
    start_urls = ["https://songsara.net/mood/epic"]

    def parse(self, response):
        
        # get all albums
        albums = response.css("article.postbox-i")
        
        # go to a special album and get information
        for album in albums:
            relative_url = album.css("div.post-img-hover a::attr(href)").get()
            
            if relative_url is not None:
                yield response.follow(relative_url, callback=self.parse_songs)
        
        # go to next pages - End
        next_pages = response.css("a.nextpostslink::attr(href)").get()
        
        if next_pages is not None:
            yield response.follow(next_pages, callback=self.parse)

    
    def parse_songs(self, response):
        """
        Get public information fields : image, title, artist, songs_url ...
        """
        
        # get album
        album = response.css("article.postbox-single")
        
        # get fields
        image = album.css("figure.pic-s img.attachment-pic-single::attr(src)").get()
        title = album.css("h2.AL-Si::text").get()
        artist = album.css("div.AR-Si a::text").get()
        songs_url = album.xpath("//ul[@class='audioplayer-audios']/li/@data-src").extract()
        
        # Check if the image URL is invalid and use the fallback selector if needed
        if image and image.startswith("data:"):
            image = album.css("figure.pic-s img.attachment-pic-single::attr(data-lazy-src)").get()
        
        # clone data
        yield {
            "url": response.url,
            "image": image,
            "title": title,
            "artist": artist,
            "songs": songs_url,
        }
