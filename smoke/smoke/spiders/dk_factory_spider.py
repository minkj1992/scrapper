import re

import scrapy
from scrapy.selector import SelectorList

from .. import utils, settings
from ..items import SmokeLiquidCategoryEnum, SmokeLiquidItem

login_form_data = {
    'member_id': settings.DK_FACTORY_USER_ID,
    'member_passwd': settings.DK_FACTORY_USER_PW
}


class DkMouthSpider(scrapy.Spider):
    name = "mouth"

    BASE_URL = "https://dkfactory.co.kr"
    LOGIN_URL = f"{BASE_URL}/exec/front/Member/login/"
    MOUTH_URL = f"{BASE_URL}/category/입호흡podcsv/529/?cate_no=529&sort_method=6"  # 입호흡 (인기순 정렬)
    PAGES = ['#Product_ListMenu', *[f'&page={i}' for i in range(2, 10)]]
    PAGE_SIZE = 50

    def start_requests(self):
        yield scrapy.FormRequest(DkMouthSpider.LOGIN_URL,
                                 formdata=login_form_data,
                                 callback=self.after_login)

    def after_login(self, response):
        for idx, page in enumerate(DkMouthSpider.PAGES):
            yield scrapy.Request(
                url=f'{DkMouthSpider.MOUTH_URL}{page}',
                callback=self.parse,
                cb_kwargs={'page': idx})

    @utils.show_locals
    def parse(self, response, page):
        base_idx = (page * DkMouthSpider.PAGE_SIZE) + 1

        products: SelectorList = response.css(
            '#contents > div.mall_center > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div > span')

        for i, product in enumerate(products):
            raw_product_name = self._get_product_name(product)
            yield SmokeLiquidItem(id=base_idx + i,
                                  name=self._parse_product_name(raw_product_name),
                                  brand=self._parse_brand_name(raw_product_name),
                                  category=SmokeLiquidCategoryEnum.MOUTH,
                                  volume=self._parse_product_volume(raw_product_name),
                                  price=self._get_product_price(product),
                                  vg=self._parse_product_nicotine_vg(raw_product_name),
                                  url=self._get_product_link(product),
                                  img_url=self._get_product_img_url(product))

    def _get_product_link(self, product: SelectorList):
        return f"{DkMouthSpider.BASE_URL}{product.css('div > a::attr(href)').get()}"

    def _get_product_img_url(self, product: SelectorList):
        return f"https:{product.css('div > a > img::attr(src)').get()}"

    def _get_product_name(self, product: SelectorList):
        return product.css('span > div.item_name.left > a *::text').get()

    def _get_product_price(self, product: SelectorList) -> int:
        origin_price = product.css('span > ul > li:nth-child(1) > span:nth-child(2)::text').get()
        discount_price = product.css('span > ul > li:nth-child(2) > span:nth-child(2)::text').get()
        price = discount_price if discount_price[-1] == '원' else origin_price
        return int(price[:-1].replace(',', ''))

    def _parse_brand_name(self, raw_product_name) -> str:
        return re.search(r'(?<=\[)[^][]*(?=])', raw_product_name).group(0)

    def _parse_product_name(self, raw_product_name) -> str:
        return re.search(r'(?<=\]).*(?=\()', raw_product_name).group(0).strip()

    def _parse_product_volume(self, raw_product_name) -> int:
        volume: str = raw_product_name.split()[-1]
        return int(volume.replace('m', '').replace('l', ''))

    def _parse_product_nicotine_vg(self, raw_product_name):
        nicotine_vg: str = re.search(r'(?<=\().*(?=\))', raw_product_name).group(0)
        return int(nicotine_vg.replace('VG', ''))
