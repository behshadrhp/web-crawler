import scrapy


class PopulationByCountrySpider(scrapy.Spider):
    name = "population_by_country"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        """
        Get and return base Information on website.
        """
        
        # Get table
        countries = response.css("table tr")

        for country in countries:

            # Get fields
            id = country.xpath(".//td[1]/text()").get(),
            country_name = country.xpath(".//td[2]/a/text()").get(),
            country_link= country.xpath(".//td[2]/a/@href").get(),
            population = country.xpath(".//td[3]/text()").get(),
            yearly_change = country.xpath(".//td[4]/text()").get(),
            net_change = country.xpath(".//td[5]/text()").get(),
            density = country.xpath(".//td[6]/text()").get(),
            land_area = country.xpath(".//td[7]/text()").get(),
            migrants = country.xpath(".//td[8]/text()").get(),
            fret_rate = country.xpath(".//td[9]/text()").get(),
            med_age = country.xpath(".//td[10]/text()").get(),
            urban_pop = country.xpath(".//td[11]/text()").get(),
            world_share = country.xpath(".//td[12]/text()").get(),

            # Save data
            yield {
                "id": id,
                "country_name": country_name,
                "country_link": country_link,
                "population": population,
                "yearly_change": yearly_change,
                "net_change": net_change,
                "density": density,
                "land_area": land_area,
                "migrants": migrants,
                "fret_rate": fret_rate,
                "med_age": med_age,
                "urban_pop": urban_pop,
                "world_share": world_share,
            }
