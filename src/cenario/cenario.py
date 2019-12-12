from typing import Union
from pathlib import Path

from pygame import surfarray
from pygame.sprite import Sprite

from src.utils import load_image

ImagemPath = Union[Path, str]
CENARIO_SPEED = 4


class Cenario(Sprite):

    def __init__(self, imgpath):
        Sprite.__init__(self)
        self.imgPath = imgpath
        self.original, self.rect = load_image(self.imgPath)
        self.image = self.original.copy()

    def clean(self):
        self.image = self.original.copy()

    def blit(self, source, position):
        self.image.blit(source, position)
