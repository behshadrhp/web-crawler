import scrapy
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By

class HomeDealsSpider(scrapy.Spider):
    name = "home_deals"
    allowed_domains = ["slickdeals.net"]
    start_urls = ["https://slickdeals.net/deals/home/"]

    def __init__(self):
        """
        Set selenium webdriver and apply orders. 
        """

        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(2)

    def parse(self, response):
        self.driver.get(response.url)
        
        response_page = Selector(text=self.driver.page_source)

        carts = response_page.xpath("//ul[@class='bp-p-filterGrid_items']/li/div[@class='bp-c-card_content']")

        for cart in carts:
            title = cart.xpath("./a/text()").get()
            price = cart.xpath("./span[@class='bp-p-dealCard_price']/text()").get()
            subtitle = cart.xpath("./span[@class='bp-c-card_subtitle']/text()").get()
            sheared_time = cart.xpath("normalize-space(./figure/figcaption/div/span/text())").get()
            store_name = cart.xpath("normalize-space(./figure/figcaption/div/text()[2])").get()

            store = store_name.replace("by ", "")

            yield {
                "title": title,
                "price": price,
                "subtitle": subtitle,
                "sheared_time": sheared_time,
                "store": store
            }

        self.driver.close()
