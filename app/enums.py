from enum import Enum


class CLASSNAME(Enum):
    BANNER = 'banner'
    CRACK = 'crack'
    PORTHOLE = 'pothole'
    VEHICLE = 'vehicle'
    TRASH = 'trash'


class STATUS(Enum):
    WAIT = 'W'
    PROGRESS = 'P'
    COMPLETE = 'C'
