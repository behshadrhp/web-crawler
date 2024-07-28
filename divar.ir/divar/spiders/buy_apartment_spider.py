import scrapy


class BuyApartmentSpiderSpider(scrapy.Spider):
    name = "buy_apartment_spider"
    allowed_domains = ["divar.ir"]
    start_urls = ["https://divar.ir/s/tehran/buy-apartment/"]

    def parse(self, response):
        
        apartments = response.css("div.post-list__widget-col-a3fe3")
        
        for apartment in apartments:
            
            relative_url = apartment.css("div a::attr(href)").get()

            if relative_url is not None:
                yield response.follow(relative_url, callback=self.parse_apartment)

    def parse_apartment(self, response):

        # fields
        initial_fields = response.xpath("//tr[@class='kt-group-row__data-row']/td/text()").getall()
        price_fields = response.xpath("//p[@class='kt-unexpandable-row__value']/text()").getall()
        
        yield {
            "url": response.url,
            "title": response.css("div.kt-page-title__title::text").get(default=''),
            "subtitle": response.css("div.kt-page-title__subtitle::text").get(default=''),
            "estate_agent": response.css("a.kt-unexpandable-row__action::text").get(default=''),
            "page_estate_agent": response.css("a.kt-unexpandable-row__action::attr(href)").get(default=''),
            "meterage": initial_fields[0] if len(initial_fields) > 0 else '',
            "year_make": initial_fields[1] if len(initial_fields) > 1 else '',
            "rooms": initial_fields[2] if len(initial_fields) > 2 else '',
            "total_price": price_fields[0] if len(price_fields) > 0 else '',
            "price_of_meter": price_fields[1] if len(price_fields) > 1 else '',
            "floor": price_fields[2] if len(price_fields) > 2 else '',
        }
