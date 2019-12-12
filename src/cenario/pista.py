import os
import time
import numpy as np
from typing import List

from pygame import Rect, surfarray, font, draw
from pygame.sprite import Sprite

from src.agentes import Carro, ANGULO_INICIO
from src.cenario import Cenario
from src.cenario._pista_high_performance_ import preencher_matriz_colisao, preencher_matriz_distancias, \
    calcula_comprimento_pista, constroi_paredes_colisao

MAIOR_DISTANCIA_POSSIVEL = 100000
COR_LASER = [255, 0, 0]
DEGTORAD = (0.01745329251994329576)


class Pista(Cenario):

    def __init__(self, nomePista):
        pathPista = './res/images/{}.png'.format(nomePista)
        self.nomePista = nomePista
        Cenario.__init__(self, pathPista)

        self.font = font.SysFont('arial', 32)

        self.matriz_colisao = np.zeros((self.rect.width, self.rect.height), dtype=np.int)
        self.preencher_matriz_colisao()

        self.matriz_distancias = np.full((self.rect.width, self.rect.height), MAIOR_DISTANCIA_POSSIVEL, dtype=np.int)
        self.comprimento_pista = MAIOR_DISTANCIA_POSSIVEL
        self.distancia_corte = self.comprimento_pista
        self.incremento_distancia_corte = 1
        self.imagemParedesColisao = self.constroiImagemParedesColisao()

    def preencher_matriz_colisao(self):
        print('Preenchendo matriz de colisão...')
        img_array = surfarray.array3d(self.image)
        print('Iniciando preenchimento da matriz de Colisoes')
        ini = time.time()
        self.matriz_colisao = preencher_matriz_colisao(img_array, self.matriz_colisao)
        print('Matriz de Colisoes Preenchida! tempo: ', time.time() - ini)

    def preencher_matriz_distancias(self, pos_linha_chegada: Rect):
        print('Preenchendo matriz de distancias...')
        pathFile = './res/distancias/{}.npy'.format(self.nomePista)
        if os.path.exists(pathFile):
            print('Encontrado arquivo de distancias...')
            self.matriz_distancias = np.loadtxt(str(pathFile), dtype=np.int)
        else:

            x_linha = pos_linha_chegada.x
            y_linha = pos_linha_chegada.y
            img_array = surfarray.array3d(self.image)
            print('Iniciando preenchimento da matriz de distancias')
            ini = time.time()
            self.matriz_distancias = preencher_matriz_distancias(img_array, self.matriz_colisao, self.matriz_distancias,
                                                                 (x_linha, y_linha))
            print('Matriz de distrancias Preenchida! tempo: ', time.time() - ini)
            print('Salvando arquivo de distancias')
            np.savetxt(str(pathFile), self.matriz_distancias, fmt='%d')
        print('Calculando comprimento da pista')
        ini = time.time()
        self.comprimento_pista = calcula_comprimento_pista(self.matriz_distancias, self.matriz_colisao)
        print("Comprimento da pista de {} pixels\nTempo de calculo: {}".format(self.comprimento_pista, time.time() - ini))
        self.distancia_corte = self.comprimento_pista

    def verifica_distancia_corte(self, afetados: List[Sprite]):
        objsColididos = 0
        for obj in afetados:
            if self.matriz_distancias[obj.rect.x][obj.rect.y] >= self.distancia_corte:
                obj.colidiu = True
                objsColididos += 1
        if self.distancia_corte > 0:
            self.distancia_corte -= self.incremento_distancia_corte
            self.incremento_distancia_corte += 0.001

    def desenhaSensores(self, carro: Carro):
        leituraSensores = carro.ler_sensores()
        X1 = carro.rect.x
        Y1 = carro.rect.y
        for i, l in enumerate(leituraSensores[:-1]):
            angulo = (carro.angulo + 90 + ((180 / (carro.qtdSensores - 2)) * i))

            X = carro.rect.x + leituraSensores[i] * -np.cos(DEGTORAD * angulo)

            Y = carro.rect.y + leituraSensores[i] * np.sin(DEGTORAD * angulo)

            #print(f'Angulo do carro: {carro.angulo}, Angulo do laser: {angulo}')

            # X = X1 + l * np.cos(angulo * np.pi / 180)
            # Y = Y1 + l * np.sin(angulo * np.pi / 180)

            draw.line(self.image, (0, 255, 0), (X, Y), (X1, Y1))
        print('\n\n')

    def constroiImagemParedesColisao(self):
        print('Construindo parede de colisoes...')
        ini = time.time()
        paredes_colisao = constroi_paredes_colisao(self.matriz_colisao,
                                                   np.full((self.matriz_colisao.shape[0],
                                                            self.matriz_colisao.shape[1], 3),
                                                           0, dtype=np.int))
        print('Paredes de colisao construidas! {} segundos'.format(time.time() - ini))
        return surfarray.make_surface(paredes_colisao)