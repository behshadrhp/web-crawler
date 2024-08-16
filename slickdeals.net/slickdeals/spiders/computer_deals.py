import scrapy


class ComputerDealsSpider(scrapy.Spider):
    name = "computer_deals"
    allowed_domains = ["slickdeals.net"]
    start_urls = ["https://slickdeals.net/computer-deals/"]


    def parse(self, response):
        

        result = response.xpath("//ul[@class='bp-p-filterGrid_items']/li")

        for res in result:
            url = res.xpath("./div/a/@href").get()
            title = res.xpath("./div/a/text()").get()
            price = res.xpath("./div/span[@class='bp-p-dealCard_price']/text()").get()
            shared_time = res.xpath("./div/figure/figcaption/div/span/text()").get()
            store = res.xpath("normalize-space(./div/figure/figcaption/div/text()[2])").get()

            store_name = store.replace("by ", "")
            

            yield {
                "url": url,
                "title": title,
                "price": price,
                "shared_time": shared_time,
                "store": store_name
            }

