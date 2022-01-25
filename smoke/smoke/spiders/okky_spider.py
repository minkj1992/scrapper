import scrapy
from scrapy.selector import SelectorList

from ..items.okky import OkkyPostItem

PAGE_SIZE = 24
INIT_PAGE_COUNT = 500


def get_pages() -> str:
    for i in range(INIT_PAGE_COUNT):
        yield f"offset={i * PAGE_SIZE}&max={PAGE_SIZE}"


def get_post_id(page_idx, post_idx) -> int:
    return page_idx * PAGE_SIZE + post_idx


def parse_article(articles) -> str:
    result = ""
    for article in articles:
        result += article.get()
        result += '\n'
    return result


class OkkyInitSpier(scrapy.Spider):
    page_url = "https://okky.kr/articles"
    post_url = "https://okky.kr/article"
    name = "okky_init"
    category = "okky_init"

    def start_requests(self):
        for i, page in enumerate(get_pages()):
            url = f"{self.page_url}/life?query=&sort=id&order=desc&{page}"
            yield scrapy.Request(url, callback=self.parse_page, cb_kwargs={"page_idx": i})

    def parse_page(self, response, page_idx):
        posts: SelectorList = response.css("#list-article > div.panel.panel-default.life-panel > ul > li")
        for post_idx, post in enumerate(posts):
            post_id = post.css("div.list-title-wrapper.clearfix > div > span::text").get()[1:]
            url = f"{self.post_url}/{post_id}"
            yield scrapy.Request(url=url, callback=self.parse_post,
                                 cb_kwargs={"page_idx": page_idx, "post_idx": post_idx})

    def parse_post(self, response, page_idx, post_idx):
        post_id = get_post_id(page_idx, post_idx)
        title = response.css("#content-body > h2::text").get().strip()
        post_body: SelectorList = response.css("#content-body > article > p::text")

        yield OkkyPostItem(
            id=post_id,
            title=title,
            body=parse_article(post_body)
        )
