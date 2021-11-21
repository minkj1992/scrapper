from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .utils import pipe


@dataclass
class SmokeLiquidItem:
    id: int
    name: str
    brand: str
    category: SmokeLiquidCategoryEnum
    volume: int  # 용량 (ml)
    price: int
    vg: int  # 니코틴 비율 (vg: 100-vg = vg: pg)
    url: str
    img_url: str
    nicotine_category: Optional[NicotineCategoryEnum] = None
    descirption: Optional[str] = None  # 상품 설명
    menthol: Optional[MentholStrengthEnum] = None  # 멘솔 정도
    image_paths: str = ''

    def get_img_name(self):
        file_ext = 'jpg'
        category = '입' if self.category == SmokeLiquidCategoryEnum.MOUTH else '폐'
        return f"{self.id}_{category}_{self.brand}_{self.name}_{self.volume}_{self.vg}vg_{self.price}원.{file_ext}"


class SmokeLiquidCategoryEnum(str, Enum):
    MOUTH = "mouth"  # 입호흡 (PG50 : VG50)
    LUNG = "lung"  # 폐호흡 (PG30 : VG70)


class NicotineCategoryEnum(str, Enum):
    SALT = "salt"  # salt / 각종 니코틴을 흡수가 잘 되도록 정제한 니코틴
    RS = "rs"  # 합성 니코틴 / 의료용 니코틴
    TFN = "tfn"  # 합성 니코틴 / Tabacco Free Nicotine
    STEM = "stem"  # 줄기 니코틴 / 식물 담배의 줄기에서 추출한 니코틴
    TOBACO = "tobaco"  # 천연니코틴 / 식물 담배잎에서 추출한 니코틴
    FREE = "free"  # 무니코틴 / 니코틴 무


class MentholStrengthEnum(str, Enum):
    NONE = "none"  # 무
    LOW = 'low'  # 낮음
    NORMAL = "normal"  # 보통
    HIGH = "high"  # 높음


# TODO: move another dir
class NameParser:
    """
    쥬스팩토리에서 크롤링한 상품이름을 적절한 정보로 변경한다.
    """

    def __init__(self, raw_name):
        self._raw_name = raw_name
        self.name = None
        self.category = None
        self.nicotine_category = None
        self.volume = None
        self.nicotine = None

    def parse(self):
        self.do_process()

        return {
            'name': self.name,
            'category': self.category,
            'nicotine_category': self.nicotine_category,
            'volume': self.volume,
            'nicotine': self.nicotine
        }

    def do_process(self) -> deque:
        raw_name = deque(self._raw_name.split())
        output = pipe(
            raw_name,
            self._set_category,
            self._set_nicotine,
            self._set_volume,
            self._set_nicotine_category,
            self._set_name
        )
        return output

    def _set_category(self, data: deque) -> deque:
        category = data.popleft()
        self.category = category
        return data

    def _set_nicotine(self, data: deque) -> deque:
        raw_nicotine = data.pop()
        nicotine = raw_nicotine.replace('mg', '')
        self.nicotine = float(nicotine)
        return data

    def _set_volume(self, data: deque) -> deque:
        raw_volume = data.pop()
        volume = raw_volume.replace('ml', '')
        self.volume = int(volume)
        return data

    def _set_nicotine_category(self, data: deque) -> deque:
        nicotine_category = data.pop()

        if nicotine_category == '합성':
            nicotine_category = NicotineCategoryEnum.TFN
        self.nicotine_category = nicotine_category
        return data

    def _set_name(self, data: deque) -> deque:
        name_list = []
        for _ in range(len(data)):
            name_list += data.popleft()

        self.name = '_'.join(name_list)
        return data
