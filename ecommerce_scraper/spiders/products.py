import scrapy
from ecommerce_scraper.items import ProductItem

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        product_links = response.css("h3 a::attr(href)").getall()

        for product_link in product_links:
            yield response.follow(product_link, self.parse_product)

        # Follow pagination links
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_product(self, response):
        item = ProductItem()
        item["title"] = response.css("h1::text").get()
        item["price"] = response.css("p.price_color::text").get()
        item["description"] = response.css("meta[name='description']::attr(content)").get()
        yield item


