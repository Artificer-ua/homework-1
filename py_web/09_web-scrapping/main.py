import json
import logging

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Field, Item

from seeds import AUTHORS, QUOTES, seed_authors, seed_quotes

logging.getLogger("scrapy").setLevel(
    logging.WARNING
)  # reduce log level for pika because of...


class QuoteItem(Item):
    tags = Field()
    author = Field()
    text = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(
                {
                    "fullname": adapter["fullname"],
                    "born_date": adapter["born_date"],
                    "born_location": adapter["born_location"],
                    "description": adapter["description"],
                }
            )
        if "author" in adapter.keys():
            self.quotes.append(
                {
                    "tags": adapter["tags"],
                    "author": adapter["author"],
                    "quote": adapter["text"],
                }
            )
        return item

    def close_spider(self, spider):
        with open(AUTHORS, "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False)
        logging.info(f"File {AUTHORS} is created.")

        with open(QUOTES, "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False)
        logging.info(f"File {QUOTES} is created.")


class QuotesSpider(scrapy.Spider):
    name = "Quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {QuotesPipeline: 300}}

    def parse(self, response, *_):
        logging.info(f"Starting scrapping {self.start_urls}")
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, text=q)
            yield response.follow(
                url=self.start_urls[0] + quote.xpath("span/a/@href").get(),
                callback=self.nested_parse_author,
            )

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield scrapy.Request(url=self.start_urls[0] + next_page)

    def nested_parse_author(self, response, *_):
        author = response.xpath("/html//div[@class='author-details']")

        fullname = author.xpath("h3[@class='author-title']/text()").get().strip()

        born_date = (
            author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        )

        born_location = (
            author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        )

        description = (
            author.xpath("div[@class='author-description']/text()").get().strip()
        )

        yield AuthorItem(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    logging.info("End of scrapping.")

    seed_authors(AUTHORS)
    logging.info(f"Contents {AUTHORS} was added to DB")
    seed_quotes(QUOTES)
    logging.info(f"Contents {QUOTES} was added to DB")
