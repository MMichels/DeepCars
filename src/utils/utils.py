import os

from pygame import image, error
from pygame.locals import RLEACCEL


def load_image(path, colorkey=None):
    try:
        img = image.load(path)
    except error as message:
        print('Não foi possivel abrir a imagem: ', path)
        raise SystemExit(message)

    img = img.convert_alpha()
    if colorkey:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)
    return img, img.get_rect()