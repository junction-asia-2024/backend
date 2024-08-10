from enum import Enum


class TYPE(Enum):
    BANNER = 'banner'
    CRACK = 'crack'
    PORTHOLE = 'porthole'
    VEHICLE = 'vehicle'
    TRASH = 'trash'


class STATUS(Enum):
    WAIT = 'W'
    PROGRESS = 'P'
    COMPLETE = 'C'
