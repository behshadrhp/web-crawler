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
            
            # split data
            cover_images = album.css("figure img::attr(src)").extract()
            cover = cover_images[0] if len(cover_images) == 1 else cover_images[1]
            # None or ...
            genre_element = album.css("li.index-da a")
            genre = genre_element.attrib["href"] if genre_element else None
            artist_element = album.css("li.index-ar a")
            artist = artist_element.attrib["href"] if artist_element else None

            yield{
                "link": album.css("div.post-img-hover a").attrib["href"],
                "cover": cover,
                "type": album.css("span.TSale::text").get(),
                "title": albums.css("li.index-al::text").get(),
                "artist": artist,
                "genre": genre,
                "date": album.css("li.index-da::text").get(),
            }
        
        next_pate_element = response.css("a.nextpostslink")
        next_page = response.css("a.nextpostslink").attrib["href"] if next_pate_element else None
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
