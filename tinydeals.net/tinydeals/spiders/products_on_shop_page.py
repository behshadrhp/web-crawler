import scrapy


class ProductsOnShopPageSpider(scrapy.Spider):
    name = "products_on_shop_page"
    allowed_domains = ["www.tinydeals.net"]
    start_urls = ["https://www.tinydeals.net/shop"]

    def parse(self, response):
        """
        Get all product from shop center.
        """

        products = response.xpath("//ul/li/div[@class='product-outer product-item__outer']")

        for product in products:
            product_link = product.xpath(".//div/div/a/@href").get()
            product_title = product.xpath(".//div/div/a/h2/text()").get()
            product_price = product.xpath(".//div/div[@class='product-loop-footer product-item__footer']/div/span/span//span[contains(@class, 'woocommerce-Price-amount') and not(ancestor::del)][1]/bdi/text()").get()
            category_link = product.xpath(".//div/div/span/a/@href").get()
            category_title = product.xpath(".//div/div/span/a/text()").get()

            yield {
                "product_title": product_title,
                "price": product_price,
                "product_link": product_link,
                "category_title": category_title,
                "category_link": category_link,
            }

        next_page = response.xpath("//li/a[@class='next page-numbers']/@href").get()

        if next_page:
            yield response.follow(url=next_page, callback=self.parse)
