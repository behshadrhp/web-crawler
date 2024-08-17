import scrapy
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ComputerDealsSpider(scrapy.Spider):
    name = "computer_deals"
    allowed_domains = ["slickdeals.net"]
    start_urls = ["https://slickdeals.net/computer-deals/"]

    def __init__(self):
        """
        Open Selenium WebDriver and apply orders.
        """
        self.driver = webdriver.Firefox()
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(3)

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            # Extract data from the current page
            response_page = Selector(text=self.driver.page_source)
            result = response_page.xpath("//ul[@class='bp-p-filterGrid_items']/li")

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

            # Try to go to the next page
            try:
                next_page_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "bp-c-pagination_right"))
                )
                next_page_button.click()
            except:
                break

        # Close the driver after the loop
        self.driver.close()
