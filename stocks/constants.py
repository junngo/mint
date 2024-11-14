from enum import Enum

class MarketType(Enum):
    KOSPI = 'KOSPI'
    KOSDAQ = 'KOSDAQ'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    @classmethod
    def get_display_name(cls, code):
        try:
            return cls[code].value
        except KeyError:
            return "알 수 없음"
