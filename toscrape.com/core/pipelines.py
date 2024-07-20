from itemadapter import ItemAdapter


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