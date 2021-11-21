from smoke.smoke.spiders.dk_factory_spider import DkMouthSpider

raw_name = "■ [오지구OG9] 고드름 소다 (50VG) 30ml"
dk_mouth_spider = DkMouthSpider()


def test_parse_brand_name():
    output = dk_mouth_spider.parse_brand_name(raw_name)
    assert output == '오지구OG9'


def test_parse_product_name():
    output = dk_mouth_spider.parse_product_name(raw_name)
    assert output == '고드름 소다'


def test_parse_product_volume():
    output = dk_mouth_spider.parse_product_volume(raw_name)
    assert output == 30


def test_parse_product_nicotine_vg():
    output = dk_mouth_spider.parse_product_nicotine_vg(raw_name)
    assert output == 50
