import datetime

from naver_tour.spiders import utils
from rich.console import Console
import scrapy
from scrapy.selector import SelectorList

# from ..items import NaverTourItem
console = Console()

NUM_OF_ADULT = 1
LOC_FROM = "ICN"
LOC_TO = "MSP"
START_AT = '20221101'
END_AT = '20221231'

BASE_URL = "https://flight.naver.com/flights/international"
IS_DIRECT = str(True).lower()
FARE_TYPE = 'Y'


def get_url_by_date(start_date: str, end_date: str):
    return f'{BASE_URL}/{LOC_FROM}-{LOC_TO}-{start_date}/{LOC_TO}-{LOC_FROM}-{end_date}?adult={NUM_OF_ADULT}&isDirect={IS_DIRECT}&fareType={FARE_TYPE}'


class NaverTourSpier(scrapy.Spider):
    name = "naver_tour"

    def start_requests(self):
        for s, e in utils.date_iter(START_AT, END_AT):
            url = get_url_by_date(s, e)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        console.print(response.text)
        # posts: SelectorList = response.css("#list-article > div.panel.panel-default.life-panel > ul > li")
        # for post_idx, post in enumerate(posts):
        #     post_id = post.css("div.list-title-wrapper.clearfix > div > span::text").get()[1:]
        #     url = f"{self.post_url}/{post_id}"
        #     yield scrapy.Request(url=url, callback=self.parse_post,
        #                          cb_kwargs={"page_idx": page_idx, "post_idx": post_idx})

    # def parse_post(self, response, page_idx, post_idx):
    #     post_id = get_post_id(page_idx, post_idx)
    #     title = response.css("#content-body > h2::text").get().strip()
    #     post_body: SelectorList = response.css("#content-body > article > p::text")

    #     yield OkkyPostItem(
    #         id=post_id,
    #         title=title,
    #         body=parse_article(post_body)
    #     )
