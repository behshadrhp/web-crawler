import scrapy


class PopulationByCountryGetDetailInformationSpider(scrapy.Spider):
    name = "population_by_country_get_detail_information"
    allowed_domains = ["www.worldometers.info"]
    start_urls = ["https://www.worldometers.info/world-population/population-by-country/"]

    def parse(self, response):
        """
        Get all information about population by countries.
        """

        countries = response.css("table tr")

        for country in countries:

            # get link
            country_link = country.xpath(".//td/a/@href").get()

            # convert to valid path
            absolute_link = f"https://www.worldometers.info{country_link}"

            yield response.follow(url=absolute_link, callback=self.parse_country_population)


    def parse_country_population(self, response):
        """
        Get Detailed Information form special pages.
        """
        
        # fields form page
        country_name = response.xpath("//div/ul/li[6]/text()").get()
        population_by_city = response.xpath("//div[14][@class='table-responsive']/table/tbody")

        for city in population_by_city:
            city_name = city.xpath(".//td[2]/text()").get()
            city_population = city.xpath(".//td[3]/text()").get()

            yield {
                "country_name": country_name,
                "city_name": city_name,
                "city_population": city_population
            }
