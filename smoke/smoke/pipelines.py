import scrapy
from scrapy.pipelines.images import ImagesPipeline

from .items import SmokeLiquidItem


class SmokeLiquidItemImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        folder_name = item.category
        return f'{folder_name}/{item.image_name}'

    def get_media_requests(self, item: SmokeLiquidItem, info):
        meta = {'filename': item.image_name}
        yield scrapy.Request(url=item.img_url, meta=meta)
