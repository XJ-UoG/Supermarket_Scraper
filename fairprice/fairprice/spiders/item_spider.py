import scrapy
from scrapy.http import Request

class ItemSpiderSpider(scrapy.Spider):
    name = 'item_spider'
    allowed_domains = ['webscraper.io']
    start_urls = ["https://webscraper.io/test-sites/e-commerce/allinone"]

    def parse(self, response):
        # Extract side-menu links
        side_menu_links = response.css('a.category-link::attr(href)').getall()
        for link in side_menu_links:
            if link:
                absolute_url = response.urljoin(link)
                # Use meta to indicate that Selenium should handle this request
                yield Request(absolute_url, callback=self.parse_category, meta={'selenium': True})

    def parse_category(self, response):
        # Extract subcategory links within the category page
        subcategory_links = response.css('a.subcategory-link::attr(href)').getall()
        for link in subcategory_links:
            if link:
                absolute_url = response.urljoin(link)
                # Use meta to indicate that Selenium should handle this request
                yield Request(absolute_url, callback=self.parse_subcategory, meta={'selenium': True})

    def parse_subcategory(self, response):
        self.logger.info(f"Visited subcategory: {response.url}")
        # Iterate through each div with class 'row'
        for row in response.css('div.row'):
            # Check if the row contains div elements with classes 'col-md-4 col-xl-4 col-lg-4'
            for product in row.css('div.col-md-4.col-xl-4.col-lg-4'):
                # Extract the product name and hyperlink
                item_name = product.css('a.title::text').get()
                item_link = product.css('a.title::attr(href)').get()
                if item_name and item_link:
                    yield {
                        "item_name": item_name,
                        "item_link": response.urljoin(item_link)  # Convert relative URL to absolute URL
                    }
