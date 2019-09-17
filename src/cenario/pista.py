import numpy as np

from pathlib import Path

from pygame import Rect
from pygame import surfarray

from src.cenario import Cenario
from src.cenario._pista_high_performance_ import preencher_matriz_colisao, preencher_matriz_distancias, \
    encontrar_maior_distancia

MAIOR_DISTANCIA_POSSIVEL = 99999999


class Pista(Cenario):

    def __init__(self, nomePista):
        pathPista = './res/images/{}.png'.format(nomePista)
        self.nomePista = nomePista
        Cenario.__init__(self, pathPista)
        self.matriz_colisao = np.zeros((self.rect.width, self.rect.height), dtype=np.int)
        self.matriz_distancias = np.full((self.rect.width, self.rect.height), MAIOR_DISTANCIA_POSSIVEL, dtype=np.int)
        self.preencher_matriz_colisao()

        self.maior_distancia = 0

    def preencher_matriz_colisao(self):
        print('Preenchendo matriz de colisão...')
        img_array = surfarray.array3d(self.image)
        self.matriz_colisao = preencher_matriz_colisao(img_array, self.matriz_colisao)

    def preencher_matriz_distancias(self, pos_linha_chegada: Rect):
        print('Preenchendo matriz de distancias...')
        pathDistancias = Path('./res/distancias/{}.npy'.format(self.nomePista))
        if pathDistancias.exists():
            print('Encontrado arquivo de distancias...')
            self.matriz_distancias = np.load(str(pathDistancias.absolute()))
        else:

            x_linha = pos_linha_chegada.x
            y_linha = pos_linha_chegada.y
            img_array = surfarray.array3d(self.image)
            self.matriz_distancias = preencher_matriz_distancias(img_array, self.matriz_colisao, self.matriz_distancias,
                                                                 (x_linha, y_linha))
            print('Salvando arquivo de distancias')
            np.save(str(pathDistancias.absolute()), self.matriz_distancias)
