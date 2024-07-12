import scrapy


class BuyApartmentSpiderSpider(scrapy.Spider):
    name = "buy_apartment_spider"
    allowed_domains = ["divar.ir"]
    start_urls = ["https://divar.ir/s/tehran/buy-apartment/"]

    def parse(self, response):
        
        apartments = response.css("div.post-list__widget-col-a3fe3")
        
        for apartment in apartments:
            yield{
                "url": apartment.css("div a").attrib["href"],
                "title": apartment.css("h2.kt-post-card__title::text").get(),
                "price": apartment.css("div.kt-post-card__description::text").get(),
                "image": apartment.css("div img.kt-image-block__image").attrib["data-src"],
                "created_by": apartment.css("span.kt-post-card__bottom-description::text").get(),
            }
