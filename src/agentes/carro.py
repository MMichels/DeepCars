from random import randint
from typing import List
import copy

import numpy as np
from pygame import transform
from pygame import font
from pygame.sprite import Sprite
from pygame.locals import *

#from cyrebro import PyDensa
#from src.cerebro.fails.redeNeural import RedeNeural
#from src.cerebro.Keural import Keural
from src.cerebro.Torcerebro import Torcerebro
from src.utils import load_image
from src.utils.logDuracao import listaTempos

font.init()

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

ANGULO_INICIO = 90
SPEED = 0
VELOCIDADE_MAXIMA = 4
QTD_SENSORES = 18
QTD_CAMADAS_ESCONDIDAS = 1
QTD_NEURONIOS_CAMADA_ESCONDIDA = 6
QTD_NEURONIOS_CAMADA_SAIDA = 4
DEGTORAD = (0.01745329251994329576)


class Carro(Sprite):

    def __init__(self, matrizColisao, matrizDistancias, posicaoFaixa):
        Sprite.__init__(self)

        self.matrizColisao = matrizColisao
        self.matrizDistancias = matrizDistancias
        self.posicaoFaixa = posicaoFaixa
        self.passouFaixa = False
        self.colidiu = False
        self.angulo = ANGULO_INICIO
        self.velocidade = SPEED
        self.velocidadeX = 0
        self.velocidadeY = 0
        self.qtdSensores = QTD_SENSORES
        self.sensoresDistancia = np.zeros(self.qtdSensores)
        self.fitness = 0;

        esteCarro = randint(0, len(POSIVEIS_CARROS.keys()) - 1)
        self.original, self.rect_original = load_image(POSIVEIS_CARROS[esteCarro], -1)
        self.image, self.rect = self._redimenciona_rotaciona()
        self.font = font.SysFont('arial', 20)

        #self.cerebro = PyDensa(QTD_SENSORES, QTD_CAMADAS_ESCONDIDAS, QTD_NEURONIOS_CAMADA_ESCONDIDA,
        #                       QTD_NEURONIOS_CAMADA_SAIDA)
        #self.cerebro = RedeNeural(18, 6, 1, 4)
        #self.cerebro = Keural(self.qtdSensores, QTD_CAMADAS_ESCONDIDAS, QTD_NEURONIOS_CAMADA_ESCONDIDA, QTD_NEURONIOS_CAMADA_SAIDA)
        
        self.cerebro = Torcerebro(QTD_SENSORES, QTD_CAMADAS_ESCONDIDAS, QTD_NEURONIOS_CAMADA_ESCONDIDA, QTD_NEURONIOS_CAMADA_SAIDA)
        self.respostaCerebro = [0, 0, 0, 0]
        self._carregaMelhorCerebro()

    def _redimenciona_rotaciona(self):
        novasDimensoes = int(self.rect_original.width * PORCENTAGEM_TAMANHO_CARROS), \
                         int(self.rect_original.height * PORCENTAGEM_TAMANHO_CARROS)
        self.image = transform.scale(self.original, novasDimensoes)
        self.image = transform.rotate(self.image, self.angulo-ANGULO_INICIO)
        self.image.set_alpha(0)
        return self.image, self.image.get_rect()

    def _carregaMelhorCerebro(self):
        import os
        if os.path.exists('./res/DNA/melhorDNA.txt'):
            melhorDna = np.loadtxt('./res/DNA/melhorDNA.txt')
            self.cerebro.colarDNA(melhorDna)


    def escreve_distancia(self):
        distancia = self.matrizDistancias[self.rect.centerx][self.rect.centery]
        text = self.font.render(f'{distancia}', 1, (200, 200, 200))
        textRect = text.get_rect(centerx=self.image.get_width() / 2,
                                 centery=self.image.get_height() / 2)
        self.image.blit(text, textRect)

    def incrementa_velocidade(self, taxa=0.2):
        self.velocidade -= taxa
        if self.velocidade > VELOCIDADE_MAXIMA:
            self.velocidade = VELOCIDADE_MAXIMA

    def decrementa_velocidade(self, taxa=0.2):
        self.velocidade += taxa
        if self.velocidade < -VELOCIDADE_MAXIMA:
            self.velocidade = -VELOCIDADE_MAXIMA;

    def rotaciona_direita(self, taxa=5.0):
        self.angulo -= taxa
        self.image, _ = self._redimenciona_rotaciona()

    def rotaciona_esquerda(self, taxa=5.0):
        self.angulo += taxa
        self.image, _ = self._redimenciona_rotaciona()

    def movimentar_manualmente(self, event):
        if event.key in [K_a, K_d, K_w, K_s]:
            if event.key == K_w:
                self.incrementa_velocidade()
            elif event.key == K_s:
                self.decrementa_velocidade()
            elif event.key == K_a:
                self.rotaciona_esquerda()
            elif event.key == K_d:
                self.rotaciona_direita()

    def ler_sensores(self, matrizColisao=None):
        if matrizColisao is None:
            matrizColisao = self.matrizColisao

        # Realiza os calculos dos sensores nas laterais do carro para verificar qual a distancia até as paredes
        # e obstaculos proximos
        leituras = np.zeros(self.qtdSensores)
        for i in range(self.qtdSensores - 1):
            x1 = self.rect.x
            y1 = self.rect.y
            '''
            Angulo = carro->Angulo - 90.0 + ((double)i) * 180.0 / ((double)(CAR_BRAIN_QTD_INPUT - 2));

            double
            Adjacente = 1 * (cos(Angulo * M_PI / 180.0));
            double
            Oposto = 1 * (sin(Angulo * M_PI / 180.0));'''

            angulo = self.angulo+ 90 + (i * 180 / (self.qtdSensores - 2))

            adjacente = -1 * (np.cos(angulo * np.pi / 180))
            oposto = 1 * (np.sin(angulo * np.pi / 180))
            while True:
                # Aqui é aonde o sensor vai lendo cada proximo pixel do mapa até encontrar uma barreira
                x1 += adjacente
                y1 += oposto
                if (matrizColisao[int(x1)][int(y1)]) == 0:
                    # Encontrou uma parede / obstaculo
                    x1 -= adjacente
                    y1 -= oposto
                    distancia = np.sqrt(
                        np.power(np.subtract(self.rect.x, x1), 2) + np.power(np.subtract(self.rect.y, y1), 2))
                    leituras[i] = distancia
                    self.sensoresDistancia[i] = distancia
                    break
        leituras[i + 1] = self.velocidade
        return leituras

    def tomarDecisoes(self, respostaCerebro: list):
        if respostaCerebro[0] > 0:  # acelerar
            self.incrementa_velocidade()

        if respostaCerebro[1] > 0:  # freiar
            self.decrementa_velocidade()

        if respostaCerebro[2] > 0:  # direita
            self.rotaciona_direita()

        if respostaCerebro[3] > 0:  # esquerda
            self.rotaciona_esquerda()

    def inferirCerebro(self):
        leituraSensores = self.ler_sensores(self.matrizColisao)
        self.cerebro.aplicarEntrada(leituraSensores)
        self.cerebro.calculaSaida()
        self.respostaCerebro = self.cerebro.obterSaida()

    def corrigePosicaoNaPista(self, pistaRect):
        antigoTop = self.rect.top
        antigoLeft = self.rect.left
        self.rect.top += pistaRect.top
        self.rect.left += pistaRect.left
        return antigoTop, antigoLeft

    def update(self):
        if not self.colidiu:
            self.inferirCerebro()
            self.tomarDecisoes(self.respostaCerebro)

            self.velocidadeX = - np.cos(np.deg2rad(self.angulo)) * self.velocidade
            self.velocidadeY = np.sin(np.deg2rad(self.angulo)) * self.velocidade

            # Verifica se ocorreu colisao
            if (self.matrizColisao[self.rect.centerx + int(self.velocidadeX),
                                   self.rect.centery + int(self.velocidadeY)]) == 0:
                self.colidiu = True

            elif (self.matrizColisao[self.rect.centerx + int(self.velocidadeX), self.rect.centery + int(self.velocidadeY)]) == 1:
                # não colidiu, pode mover
                self.rect.centerx = self.rect.centerx + int(self.velocidadeX)
                self.rect.centery = self.rect.centery + int(self.velocidadeY)

            self.escreve_distancia()

            if not self.passouFaixa:
                if self.rect.top <= self.posicaoFaixa.top:
                    self.passouFaixa = True

    def reiniciar(self):
        self.passouFaixa = False
        self.colidiu = False
        self.angulo = ANGULO_INICIO
        self.velocidade = SPEED
        self.velocidadeX = 0
        self.velocidadeY = 0
        self.sensoresDistancia = np.zeros(self.qtdSensores)
        self.fitness = 0;

        self.image, self.rect = self._redimenciona_rotaciona()
        self.respostaCerebro = [0, 0, 0, 0]

    @staticmethod
    def buscarMelhorCarro(carros, matrizDistancias, maxDistancia):
        menor = carros[0]
        menorDistancia = matrizDistancias[carros[0].rect.centerx, carros[0].rect.centery]
        for c in carros[1:]:
            distanciaEste = matrizDistancias[c.rect.centerx, c.rect.centery]
            if not c.passouFaixa:
                distanciaEste += maxDistancia
            if distanciaEste < menorDistancia:
                menor = c
                menorDistancia = distanciaEste
        return menor

    @staticmethod
    def buscarMelhorCarroVivo(carros, matrizDistancias):
        carrosVivos = [c for c in carros if not c.colidiu]
        return Carro.buscarMelhorCarro(carrosVivos, matrizDistancias)

    @staticmethod
    def calculaFitness(carros, maiorDistancia, matrizDistancias):
        for c in carros:
            c.fitness = maiorDistancia - matrizDistancias[c.rect.centerx][c.rect.centery]

    @staticmethod
    def buscarMelhorFitness(carros):
        maior = carros[0]
        for c in carros[1:]:
            if c.fitness > maior.fitness:
                maior = c
        return maior

    @staticmethod
    def verificaPassouFaixa(carros):
        return True in [c.passouFaixa for c in carros]

    @staticmethod
    def contaCarrosColididos(carros):
        i = 0
        for c in carros:
            if c.colidiu:
                i += 1
        return i

    @staticmethod
    def colidirRetardatarios(carros):
        for c in carros:
            if not c.passouFaixa:
                c.colidiu = True

    @staticmethod
    def realizarMutacao(carros: list, taxa_carros_mutacao=None):
        if taxa_carros_mutacao is None:
            taxa_carros_mutacao = int(len(carros) * 0.25)
        # Ordena od individuos de acordo com a distancia que conseguiram percorrer
        carros.sort(key=lambda x: x.fitness)
        indiceMelhorEquivalente = 0
        for i in range(taxa_carros_mutacao):
            carros[i].cerebro.copiarRede(carros[-(i+1)].cerebro)
        for i in range(len(carros) - taxa_carros_mutacao):
            carros[i].cerebro.sofrerMutacao()

        return carros
