import scrapy


class Juice24Spider(scrapy.Spider):
    name = "mouth"
    page = range(1, 16)  # 1...15
    base_url = "http://juice24.kr"
    mouth_url = f"{base_url}/category/%EC%9E%85%ED%98%B8%ED%9D%A1-%EC%83%81%ED%92%88/48/"  # 입호흡
    PAGE_SIZE = 20

    def start_requests(self):
        urls = [f'{Juice24Spider.mouth_url}/page={p}' for p in Juice24Spider.page]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)