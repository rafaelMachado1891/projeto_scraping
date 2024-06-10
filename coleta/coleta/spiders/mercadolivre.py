import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["http://lista.mercadolivre.com.br/"]

    def parse(self, response):
        pass
