import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/luminarias"]
    page_count = 1
    max_pages = 50

    def parse(self, response):
        products = response.css('div.ui-search-result__wrapper')
        for product in products:
            price = product.css('span.andes-money-amount__fraction::text').get()
            cents = product.css('span.andes-money-amount__cents::text').get()

            price_int = int(price) if price else 0
            cents_int = int(cents) if cents else 0

            yield {
                'image': product.css('div.ui-search-result__image img::attr(data-src)').get() or product.css('div.ui-search-result__image img::attr(src)').get(),
                'produto': product.css('h2.ui-search-item__title::text').get(),
                'preco': price_int,
                'cents': cents_int,
                'loja': product.css('p.ui-search-official-store-label::text').get(),
                'reviews rating number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews amount': product.css('span.ui-search-reviews__amount::text').get()
            }

        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
