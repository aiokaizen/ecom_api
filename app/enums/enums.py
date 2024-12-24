from enum import Enum


class PropertyTypeEnum(str, Enum):
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    storage = "storage"
    screen = "screen"
    battery = "battery"
    camera = "camera"
