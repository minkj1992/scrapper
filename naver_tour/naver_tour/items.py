# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

import scrapy


@dataclass
class NaverTourItem:
    uuid: str
    start_at: str
    end_at: str
    price: str
