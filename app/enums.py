from enum import Enum


class CLASSNAME(Enum):
    banner = 'banner'
    crack = 'crack'
    pothole = 'pothole'
    vehicle = 'vehicle'
    trash = 'trash'


class STATUS(Enum):
    WAIT = 'W'
    PROGRESS = 'P'
    COMPLETE = 'C'
