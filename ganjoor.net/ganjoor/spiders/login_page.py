import scrapy
from scrapy import FormRequest

class LoginPageSpider(scrapy.Spider):
    name = "login_page"
    allowed_domains = ["ganjoor.net"]
    start_urls = ["https://ganjoor.net/login"]

    def parse(self, response):
        
        yield FormRequest.from_response(
            response,
            formxpath="//form",
            formdata={
                "LoginViewModel.Username": "username",
                "LoginViewModel.Password": "password"
            },
            callback=self.after_login
        )

    def after_login(self, response):
        name = response.xpath("//tr/td[1]/text()").get()
        
        if name:
            
            print(f"login is successful -> {name}")
