import sys
from random import randint
from typing import List

import pygame


from src.cenario import Pista
from src.cenario import preencherCenarioOpt
from src.agentes import Carro

from src.utils import load_image

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

pygame.init()

screen = pygame.display.set_mode((1403, 1351))

pista = Pista('pista')

faixa, faixa_pos = load_image('./res/images/faixa.png')
faixa_pos.topleft = 245, 270

carros = [Carro() for c in range(10)]
# carro = Carro()

posiciona_carros_atras_da_faixa(faixa_pos, carros)

renderCarros = pygame.sprite.RenderPlain(carros)

clock = pygame.time.Clock()

sprites = [[faixa, faixa_pos]]

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    screen.fill([0, 0, 0])

    arrayImgCenario = pygame.surfarray.array3d(pista.image)
    imgItens = [pygame.surfarray.array3d(faixa)]
    posItens = [[faixa_pos.top, faixa_pos.left, faixa_pos.bottom, faixa_pos.right], ]
    for c in renderCarros.sprites():
        arrayImgSprite = pygame.surfarray.array3d(c.image)
        posSprite = [c.rect.top, c.rect.left, c.rect.bottom, c.rect.right]
        imgItens.append(arrayImgSprite)
        posItens.append(posSprite)

    arrayCena = preencherCenarioOpt(arrayImgCenario, imgItens, posItens)
    cena = pygame.surfarray.make_surface(arrayCena)
    pygame.image.save(cena, './testes_proto/teste.png')
    screen.blit(cena, (0, 0))
    break
