import scrapy
from scrapy.pipelines.images import ImagesPipeline

from .items import SmokeLiquidItem


class SmokeLiquidItemImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        folder_name = item.category
        return f'{folder_name}/{item.get_img_name()}'

    def get_media_requests(self, item: SmokeLiquidItem, info):
        meta = {'filename': item.get_img_name()}
        yield scrapy.Request(url=item.img_url, meta=meta)
