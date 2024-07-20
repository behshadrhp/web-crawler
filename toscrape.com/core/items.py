import scrapy


class CoreItem(scrapy.Item):
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    """
    This class is for create Book Item.
    """
    
    # initial fields
    url = scrapy.Field()
    image = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    stars = scrapy.Field()
    price = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    description = scrapy.Field()
