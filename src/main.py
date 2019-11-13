import sys
import os
import numpy as np

from random import randint
from typing import List

import pygame
from pygame.locals import *
import pygame.surfarray as sfarray

from src.cenario import Pista
from src.agentes import Carro
from src.camera import Camera
from src.utils import load_image

x_window_pos = 30
y_window_pos = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(x_window_pos, y_window_pos)

def posiciona_carros_atras_da_faixa(posicao_faixa: pygame.Rect, carros: List[Carro]):
    for carro in carros:
        bottom_faixa = posicao_faixa.bottom
        left_faixa = posicao_faixa.left
        largura_faixa = posicao_faixa.height
        altura_faixa = posicao_faixa.width

        topo_carro = randint(bottom_faixa, bottom_faixa + altura_faixa * 2)
        esquerda_carro = randint(left_faixa, left_faixa + largura_faixa)

        carro.rect.top = topo_carro
        carro.rect.left = esquerda_carro + carro.rect.height / 2

def limpar_eventos():
    pygame.event.clear()

pygame.init()

screen = pygame.display.set_mode((1400, 1000))

pista = Pista('pista')
camera = Camera(pista)

faixa, faixa_pos = load_image('./res/images/faixa.png')
faixa_pos.topleft = 245, 270

pista.preencher_matriz_distancias(faixa_pos)

carros = [Carro() for c in range(10)]
#carro = Carro()

posiciona_carros_atras_da_faixa(faixa_pos, carros)

renderCarros = pygame.sprite.RenderPlain(carros)

clock = pygame.time.Clock()

while True:
    #clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type in [KEYDOWN, KEYUP]:
            camera.verificar_eventos(event)
            #renderCarros.movimentar_manualmente(event)

    if True in camera.camBtnStates.values():
        pista.rect = camera.mov_cenario(pista.rect)

    renderCarros.update(pista.matriz_colisao)

    pista.clean()
    pista.blit(faixa, faixa_pos)
    renderCarros.draw(pista)

    screen.fill([0, 0, 0])
    screen.blit(pista.image, pista.rect)

    pygame.display.update()
