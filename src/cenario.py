from typing import Union
from pathlib import Path

from pygame import image

ImagemPath = Union[Path, str]


class Cenario:

    def __init__(self, imgpath):
        self.img = image.load(imgpath)
        self.position = self.img.get_rect()

