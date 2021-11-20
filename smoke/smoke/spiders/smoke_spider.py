import scrapy
from smoke import settings, utils


class QuotesSpider(scrapy.Spider):
    name = "쥬스팩토리_입호흡"

    def start_requests(self):
        urls = [
            f'{settings.BASE_JUICE_URL}?productListFilter=241674',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    @utils.show_locals
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        utils.print_locals()