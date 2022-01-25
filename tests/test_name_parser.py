from collections import deque

from apps.app.items.smoke import NameParser

raw_name = "입호흡 스톰리퀴드 골드씬 액상 합성 30ml 9.8mg"


def test_do_process_returns_empty_deque():
    name_parser = NameParser(raw_name)
    output = name_parser.do_process()
    assert output == deque()


# def test_parse_returns_success():
#     name_parser = NameParser(raw_name)
#     name_parser.do_process()
#     d = name_parser.parse()
#     assert d == deque()
