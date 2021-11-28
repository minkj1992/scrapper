import re

import scrapy
from scrapy.selector import SelectorList

from .. import utils, settings
from ..items import SmokeLiquidCategoryEnum, SmokeLiquidItem

LOGIN_FORM_DATA = {
    'member_id': settings.DK_FACTORY_USER_ID,
    'member_passwd': settings.DK_FACTORY_USER_PW
}

PAGE_SIZE = 50
BASE_URL = "https://dkfactory.co.kr"
LOGIN_URL = f"{BASE_URL}/exec/front/Member/login/"
INVALID_VG = -1


class DKBaseSpier(scrapy.Spider):
    name = None
    target_url = None
    pages = None
    category = None

    def start_requests(self):
        yield scrapy.FormRequest(LOGIN_URL,
                                 formdata=LOGIN_FORM_DATA,
                                 callback=self.after_login)

    def after_login(self, response):
        for idx, page in enumerate(self.pages):
            yield scrapy.Request(
                url=f'{self.target_url}{page}',
                callback=self.parse,
                cb_kwargs={'page': idx})

    @utils.show_locals
    def parse(self, response, page):
        base_idx = (page * PAGE_SIZE) + 1

        products: SelectorList = response.css(
            '#contents > div.mall_center > div.xans-element-.xans-product.xans-product-normalpackage > div > ul > li > div > span')

        for i, product in enumerate(products):
            raw_product_name = self._get_product_name(product)
            yield SmokeLiquidItem(id=base_idx + i,
                                  name=self._parse_product_name(raw_product_name),
                                  brand=self._parse_brand_name(raw_product_name),
                                  category=self.category,
                                  volume=self._parse_product_volume(raw_product_name),
                                  price=self._get_product_price(product),
                                  vg=self._parse_product_nicotine_vg(raw_product_name),
                                  url=self._get_product_link(product),
                                  img_url=self._get_product_img_url(product))

    @staticmethod
    def _get_product_link(product: SelectorList):
        return f"{BASE_URL}{product.css('div > a::attr(href)').get()}"

    @staticmethod
    def _get_product_img_url(product: SelectorList):
        return f"https:{product.css('div > a > img::attr(src)').get()}"

    @staticmethod
    def _get_product_name(product: SelectorList):
        return product.css('span > div.item_name.left > a *::text').get()

    @staticmethod
    def _get_product_price(product: SelectorList) -> int:
        origin_price = product.css('span > ul > li:nth-child(1) > span:nth-child(2)::text').get()
        discount_price = product.css('span > ul > li:nth-child(2) > span:nth-child(2)::text').get()
        price = discount_price if discount_price[-1] == '원' else origin_price
        return int(price[:-1].replace(',', ''))

    @staticmethod
    def _parse_brand_name(raw_product_name) -> str:
        return re.search(r'(?<=\[)[^][]*(?=])', raw_product_name).group(0)

    @staticmethod
    def _parse_product_name(raw_product_name) -> str:
        return re.search(r'(?<=\]).*(?=\()', raw_product_name).group(0).strip()

    @staticmethod
    def _parse_product_volume(raw_product_name) -> int:
        volume: str = raw_product_name.split()[-1]
        return int(volume.replace('m', '').replace('l', ''))

    @staticmethod
    def _parse_product_nicotine_vg(raw_product_name):

        nicotine_vg: str = re.search(r'(?<=\().*(?=\))', raw_product_name).group(0)
        nicotine_vg.replace('VG', '')

        try:
            return int(nicotine_vg)
        except ValueError:
            return INVALID_VG


class DKLungSpider(DKBaseSpier):
    name = "dk_lung"
    target_url = f"{BASE_URL}/product/list.html?cate_no=530&sort_method=6"  # 폐호흡 (인기순 정렬)
    pages = ['#Product_ListMenu', *[f'&page={i}' for i in range(2, 4)]]
    category = SmokeLiquidCategoryEnum.LUNG


class DKMouthSpider(DKBaseSpier):
    name = "dk_mouth"
    target_url = f"{BASE_URL}/category/입호흡podcsv/529/?cate_no=529&sort_method=6"  # 입호흡 (인기순 정렬)
    pages = ['#Product_ListMenu', *[f'&page={i}' for i in range(2, 10)]]
    category = SmokeLiquidCategoryEnum.MOUTH
