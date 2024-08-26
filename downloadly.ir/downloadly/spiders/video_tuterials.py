import scrapy


class VideoTuterialsSpider(scrapy.Spider):
    name = "video_tuterials"
    allowed_domains = ["downloadly.ir"]
    start_urls = ["https://downloadly.ir/download/elearning/video-tutorials/"]

    def parse(self, response):
        
        items = response.xpath("//div[@class='vc_column-inner']/section/div/div/div/div/div/div/div/article")

        for item in items:

            title = item.xpath("./div/div/div[2]/h2/a/text()").get()
            info = item.xpath("./div/div/div[2]/div[2]/text()").get()
            page_url = item.xpath("./div/div/div[2]/h2/a/@href").get()


            yield {
                "title": title,
                "info": info,
                "page url": page_url
            }

        next_page = response.xpath("//*[@id='us_grid_1']/nav/div/a[5]/@href").get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
