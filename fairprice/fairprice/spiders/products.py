import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products"
    allowed_domains = ['fairprice.com.sg']
    start_urls = [
        'https://www.fairprice.com.sg/category/fresh-milk',
    ]

    def parse(self, response):
        if "scroll" not in response.meta:
            self.logger.debug("Requesting the page with Selenium for scrolling.")
            yield scrapy.Request(response.url, meta={'scroll': True}, callback=self.parse)
        else:
            self.logger.debug("Parsing response from URL: %s" % response.url)
            product_collection = response.css('div.sc-f0165265-6.FSCyx')
            products_links = product_collection.css('a.sc-405e7c3c-3.jAMOiw::attr(href)').getall()
            self.logger.debug(f"Found {len(products_links)} products")

            for product_link in products_links:
                full_link = response.urljoin(product_link)
                yield response.follow(full_link, self.parse_product)

    def parse_product(self, response):
        product_name = response.css('span.sc-aa673588-1.drdope::text').get()
        product_brand = response.css('a.sc-6ac8ef58-1.cISoLW::text').get()
        product_size = response.css('span.sc-aa673588-1.sc-d5ac8310-3.kzSsPC.jGBApj > span::text').get()
        product_price = response.css('span.sc-aa673588-1.sc-6ac8ef58-5.kQDEta.gbCpHo::text').get()
        product_sale = response.css('div.sc-934106e3-12.jwqOuC div.sc-934106e3-21.kVgtQW.tagWrapper > ::text').get()
        product_avail = response.css('div.sc-934106e3-13 hWHlXc span.sc-aa673588-1.dLmBub::text').get()
        product_rating = response.css('span.sc-6fe931dc-4.gnxVUm.pdp::text').get()
        product_link = response.url

        self.logger.debug(f"Scraped product: {product_name}, Brand: {product_brand}, Size: {product_size}, Price: {product_price}, Rating: {product_rating}, Link: {product_link}")

        yield {
            'product_name': product_name.strip() if product_name else None,
            'product_brand': product_brand.strip() if product_brand else None,
            'product_size': product_size.strip() if product_size else None,
            'product_price': product_price.strip() if product_price else None,
            'product_rating': product_rating.strip() if product_rating else None,
            'product_sale': product_sale.strip() if product_sale else None,
            'product_avail': product_avail.strip() if product_avail else None,
            'product_link': product_link,
        }

    def closed(self, reason):
        self.logger.debug("Spider closed: %s", reason)
