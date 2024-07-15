import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        
        books = response.css("article.product_pod")

        for book in books:
            # get more information about element
            relative_url = book.css("h3 a::attr(href)").get()
        
            # go to information page
            if relative_url is not None:
                if "catalogue/" in relative_url:
                    book_url = "http://books.toscrape.com/" + relative_url
                else:
                    book_url = "http://books.toscrape.com/catalogue/" + relative_url
                yield response.follow(book_url, callback=self.parse_book_page)
        
        
        # next page
        next_page = response.css("li.next a::attr(href)").get()
        
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = "http://books.toscrape.com/" + next_page
            else:
                next_page_url = "http://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)
        
    def parse_book_page(self, response):
        
        # get data from ...
        book = response.css(".product_page")
        table_row = response.css("table tr")
        
        # clone data
        yield{
            "url": response.url,
            "image": book.css("div.item img").attrib["src"],
            "title": book.css("div.col-sm-6 h1::text").get(),
            'category': book.xpath("//li[3]/a/text()").get(),
            'stars': book.css("div.col-sm-6 p.star-rating ").attrib["class"],
            'price': book.xpath("//p[@class='price_color']//text()").get(),
            'upc': table_row[0].css("td::text").get(),
            'product_type': table_row[1].css("td::text").get(),
            'price_excl_tax': table_row[2].css("td::text").get(),
            'price_incl_tax': table_row[3].css("td::text").get(),
            'tax': table_row[4].css("td::text").get(),
            'availability': table_row[5].css("td::text").get(),
            'num_reviews': table_row[6].css("td::text").get(),
            'description': book.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        }
