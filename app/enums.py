from enum import Enum


class CLASSNAME(Enum):
    BANNER = 'banner'
    CRACK = 'crack'
    PORTHOLE = 'porthole'
    VEHICLE = 'vehicle'
    TRASH = 'trash'


class STATUS(Enum):
    WAIT = 'W'
    PROGRESS = 'P'
    COMPLETE = 'C'
