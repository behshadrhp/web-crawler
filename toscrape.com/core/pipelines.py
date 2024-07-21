from itemadapter import ItemAdapter
from mysql import connector


class CorePipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # price --> convert to float
        price_key = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price in price_key:
            value = adapter.get(price)
            value = value.replace("£", "")
            adapter[price] = float(value)
        
        # category & product Type --> switch to lowercase
        lowercase_keys = ["category", "product_type"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
            
        # Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])
        
        # Reviews --> convert string to int
        reviews = adapter.get("num_reviews")
        adapter["num_reviews"] = int(reviews)
        
        # Stars --> convert string to int
        stars = adapter.get("stars")
        split_stars =  stars.split(' ')
        stars_value = split_stars[1].lower()
        
        if stars_value == "zero":
            adapter["stars"] = 0
        elif stars_value == "one":
            adapter["stars"] = 1
        elif stars_value == "tow":
            adapter["stars"] = 2
        elif stars_value == "three":
            adapter["stars"] = 3
        elif stars_value == "four":
            adapter["stars"] = 4
        elif stars_value == "five":
            adapter["stars"] = 5
        
        return item
    
    
class SaveToMySQLPipeline:
    """
    This class is for connect to MySQL Database,
    save objects.
    """
    
    def __init__(self):
        self.connection = connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="books",
            port="3306"
        )
        
        ## Create cursor, used to execute commands
        self.cursor = self.connection.cursor()
        
        ## Create books table if none exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)
    
    def process_item(self, item, spider):

        ## Define insert statement
        self.cursor.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"])
        ))

        ## Execute insert of data into database
        self.connection.commit()

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cursor.close()
        self.connection.close()
    