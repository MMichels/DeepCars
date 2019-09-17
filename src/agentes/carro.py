from random import randint

from pygame.sprite import Sprite
from pygame import transform

from src.utils import load_image

SPEED = (5, 0)

POSIVEIS_CARROS = {
    0: './res/images/carro0.png',
    1: './res/images/carro1.png',
    2: './res/images/carro2.png',
    3: './res/images/carro3.png',
    4: './res/images/carro4.png',
    5: './res/images/carro5.png',
    6: './res/images/carro6.png',
}

PORCENTAGEM_TAMANHO_CARROS = 0.1

anguloInicio = 90

class Carro(Sprite):

    def __init__(self):
        Sprite.__init__(self)
        esteCarro = randint(0, len(POSIVEIS_CARROS.keys()) - 1)
        self.image, self.rect = load_image(POSIVEIS_CARROS[esteCarro])
        novasDimensoes = int(self.rect.width * PORCENTAGEM_TAMANHO_CARROS), int(self.rect.height * PORCENTAGEM_TAMANHO_CARROS)
        self.image = transform.scale(self.image, novasDimensoes)
        self.image = transform.rotate(self.image, anguloInicio)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
