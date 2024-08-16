import scrapy
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.common.by import By


class SearchResultSpider(scrapy.Spider):
    name = "search_result"
    allowed_domains = ["yandex.com"]
    start_urls = ["https://yandex.com/"]

    def __init__(self):
        """
        Initialize Selenium Web Driver.
        """
        
        # set webdriver + get website
        driver = webdriver.Firefox()
        driver.get("https://yandex.com/")

        # get search box
        search_text = driver.find_element(by=By.CLASS_NAME, value="search3__input")
        search_text.send_keys("Hello World")
        search_btn = driver.find_element(by=By.CLASS_NAME, value="search3__button")
        search_btn.click()

        # wait time to get all response
        driver.implicitly_wait(1)

        self.html = driver.page_source
        driver.quit()

    def parse(self, response):
        
        # get response from selenium
        response_page = Selector(text=self.html)

        result = response_page.xpath("//ul/li/div/div/a")

        for res in result:
            url = res.xpath("./@href").get()

            yield {
                "url": url,
            }
