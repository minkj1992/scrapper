import re
import scrapy
from scrapy.selector import SelectorList

from .. import utils

PAGE_SIZE = 24
MAX_TRY_COUNT = 1000


def next_page():
    for i in range(MAX_TRY_COUNT):
        yield f"&offset={i*PAGE_SIZE}&max={PAGE_SIZE}"


class OkkySpier(scrapy.Spider):
    name = "okky"
    target_url = "https://okky.kr/articles/life?query=&sort=id&order=desc"
    category = "okky"

    def start_requests(self):
        utils.rich_print("okky")
        yield scrapy.Request(url=self.target_url, callback=self.parse)  # , cb_kwargs={"page": idx}

    def parse(self, response):
        posts: SelectorList = response.css("#list-article > div.panel.panel-default.life-panel > ul > li")

        for i, post in enumerate(posts):
            post_id = utils.rich_print(post.css("div.list-title-wrapper.clearfix > div > span::text").get())
            """
            TODO
            1. for문 돌며 not visited 이면 post id visited 넣기
            2. 해당 page detail에 들어가서 title / body scrap한다.

            또는

            1. page를 전체 다 가져온다.
            2. scrap 하는 spider따로, post 쓰는 워커 따로 관리하도록 한다.
            """
