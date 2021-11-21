import re

import scrapy
from scrapy.selector import SelectorList

from .. import utils, settings

login_form_data = {
    'member_id': settings.DK_FACTORY_USER_ID,
    'member_passwd': settings.DK_FACTORY_USER_PW
}


class DkMouthSpider(scrapy.Spider):
    name = "dk_mouth"
    base_url = "https://dkfactory.co.kr"
    login_url = f"{base_url}/exec/front/Member/login/"
    mouth_url = f"{base_url}/category/입호흡podcsv/529/?cate_no=529&sort_method=6"  # 입호흡 (인기순 정렬)
    pages = ['#Product_ListMenu', *[f'&page={i}' for i in range(2, 10)]]

    def start_requests(self):
        yield scrapy.FormRequest(DkMouthSpider.login_url,
                                 formdata=login_form_data,
                                 callback=self.after_login)

    def after_login(self, response):
        for page in DkMouthSpider.pages:
            yield scrapy.Request(
                url=f'{DkMouthSpider.mouth_url}{page}',
                callback=self.parse)

    @utils.show_locals
    def parse(self, response):
        products: SelectorList = response.css(
            '#contents > div.mall_center > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div > span')

        rich_table = utils.get_table(headers=['url', 'img_url', '브랜드명', '상품명', '용량(mg)', '니코틴(vg)', '가격', '카테고리'])

        for product in products:
            raw_product_name = self.get_product_name(product)

            product_link = self.get_product_link(product)
            img_url = self.get_product_img_url(product)
            print(img_url)
            brand_name = self.parse_brand_name(raw_product_name)
            product_name = self.parse_product_name(raw_product_name)
            volume = self.parse_product_volume(raw_product_name)
            nicotine_vg = self.parse_product_nicotine_vg(raw_product_name)  # 50
            price = self.get_product_price(product)
            category = "mouth"

            rich_table.add_row(product_link, img_url, brand_name, product_name, str(volume), str(nicotine_vg), str(price), category)
        utils.rich_print(rich_table)

    def get_product_link(self, product: SelectorList):
        return product.css('div > a::attr(href)').get()

    def get_product_img_url(self, product: SelectorList):
        return f"https:{product.css('div > a > img::attr(src)').get()}"

    def get_product_name(self, product: SelectorList):
        return product.css('span > div.item_name.left > a *::text').get()

    def get_product_price(self, product: SelectorList):
        origin_price = product.css('span > ul > li:nth-child(1) > span:nth-child(2)::text').get()
        discount_price = product.css('span > ul > li:nth-child(2) > span:nth-child(2)::text').get()
        return discount_price if discount_price[-1] == '원' else origin_price

    def parse_brand_name(self, raw_product_name) -> str:
        return re.search(r'(?<=\[)[^][]*(?=])', raw_product_name).group(0)

    def parse_product_name(self, raw_product_name) -> str:
        return re.search(r'(?<=\]).*(?=\()', raw_product_name).group(0).strip()

    def parse_product_volume(self, raw_product_name) -> int:
        volume: str = raw_product_name.split()[-1]
        return int(volume.replace('ml', ''))

    def parse_product_nicotine_vg(self, raw_product_name):
        nicotine_vg: str = re.search(r'(?<=\().*(?=\))', raw_product_name).group(0)
        return int(nicotine_vg.replace('VG', ''))
