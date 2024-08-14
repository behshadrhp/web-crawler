import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By


class SearchResualtSpider(scrapy.Spider):
    name = "search_resualt"
    allowed_domains = ["www.bing.com"]
    start_urls = ["https://www.bing.com/"]

    def __init__(self):

        driver = webdriver.Firefox()
        driver.get("https://www.bing.com/")

        search_textbox = driver.find_element(by=By.ID, value="sb_form_q")
        search_textbox.send_keys("Hello World")

        search_buttonbox = driver.find_element(by=By.ID, value="search_icon")
        search_buttonbox.click()

        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        response_page = Selector(text=self.html)

        result = response_page.xpath("//li[@class='b_algo']/h2/a")

        for res in result:
            title = res.xpath("./text()").get()
            link = res.xpath("./@href").get()

            yield {
                "title": title,
                "link": link
            }
