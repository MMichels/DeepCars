from typing import Union
from pathlib import Path
from time import time

import numpy as np
from tqdm import trange

from src.utils import load_image

from pygame import Rect
from pygame.sprite import Sprite

ImagemPath = Union[Path, str]

CENARIO_SPEED = 4

class Cenario(Sprite):

    def __init__(self, imgpath):
        Sprite.__init__(self)
        self.imgPath = imgpath
        self.image, self.rect = load_image(self.imgPath)

    def clean(self):
        self.image, _ = load_image(self.imgPath)

    def blit(self, source, position):
        self.image.blit(source, position)
