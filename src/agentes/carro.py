from random import randint

import numpy as np
from pygame.sprite import Sprite
from pygame.locals import *
from pygame import transform, Surface

from src.utils import load_image
from src.redeNeural import RedeNeural

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


class Carro(Sprite):

    def __init__(self):
        Sprite.__init__(self)

        self.colidiu = False
        self.angulo = ANGULO_INICIO
        self.velocidade = SPEED
        self.velocidadeX = 0
        self.velocidadeY = 0
        self.qtdSensores = QTD_SENSORES
        self.sensoresDistancia = np.zeros(self.qtdSensores)

        self.btnStates = {
            'W_PRESSED': False,
            'S_PRESSED': False,
            'A_PRESSED': False,
            'D_PRESSED': False,
        }

        esteCarro = randint(0, len(POSIVEIS_CARROS.keys()) - 1)
        self.original, self.rect_original = load_image(POSIVEIS_CARROS[esteCarro])

        self.image, self.rect = self._redimenciona_rotaciona()

        self.cerebro = RedeNeural(qtdNeuroniosEntrada=QTD_SENSORES,
                                  qtdNeuroniosEscondidos=QTD_NEURONIOS_CAMADA_ESCONDIDA,
                                  qtdCamadasEscondidas=QTD_CAMADAS_ESCONDIDAS,
                                  qtdNeuroniosSaida=QTD_NEURONIOS_CAMADA_SAIDA)
        self.cerebro.criarRedeNeural()
        # TODO: Optimizar set dos valores de pesos dos neuronios
        self.tamanhoDNA = self.cerebro.qtdPesosRede()
        self.DNA = np.random.uniform(-1000, 1000, self.tamanhoDNA)
        self.cerebro.copiarVetorParaCamadas(self.DNA)


    def _redimenciona_rotaciona(self):
        novasDimensoes = int(self.rect_original.width * PORCENTAGEM_TAMANHO_CARROS), \
                         int(self.rect_original.height * PORCENTAGEM_TAMANHO_CARROS)
        self.image = transform.scale(self.original, novasDimensoes)
        self.image = transform.rotate(self.image, self.angulo)
        self.image.set_alpha(0)
        return self.image, self.image.get_rect()

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
        pressionado = False
        if event.type == KEYDOWN:
            pressionado = True

        if event.key in [K_a, K_d, K_w, K_s]:
            if event.key == K_w:
                keyCode = 'W_PRESSED'
            elif event.key == K_s:
                keyCode = 'S_PRESSED'
            elif event.key == K_a:
                keyCode = 'A_PRESSED'
            elif event.key == K_d:
                keyCode = 'D_PRESSED'

            self.btnStates[keyCode] = pressionado

    def ler_sensores(self, matrizColisao):

        # Realiza os calculos dos sensores nas laterais do carro para verificar qual a distancia até as paredes
        # e obstaculos proximos
        leituras = np.zeros(self.qtdSensores)
        for i in range(self.qtdSensores-1):
            x1 = self.rect.x
            y1 = self.rect.y
            angulo = self.angulo - 90 + (i * 180) / (self.qtdSensores - 2)
            adjacente = 1 * np.cos(angulo * np.pi / 180)
            oposto = 1 * np.sin(angulo * np.pi/180)
            while True:
                # Aqui é aonde o sensor vai lendo cada proximo pixel do mapa até encontrar uma barreira
                x1 += adjacente
                y1 += oposto
                if (matrizColisao[int(x1)][int(y1)]) == 0:
                    # Encontrou uma parede / obstaculo
                    x1 -= adjacente
                    y1 -= oposto
                    distancia = np.sqrt(np.power(np.subtract(self.rect.x, x1), 2) + np.power(np.subtract(self.rect.y, y1), 2))
                    leituras[i] = distancia
                    self.sensoresDistancia[i] = distancia
                    break
        leituras[i+1] = self.velocidade
        return leituras

    def tomarDecisoes(self, respostaCerebro: list):
        if respostaCerebro[0] > 0: # acelerar
            self.incrementa_velocidade()

        if respostaCerebro[1] > 0: # freiar
            self.decrementa_velocidade()

        if respostaCerebro[2] > 0: # direita
            self.rotaciona_direita()

        if respostaCerebro[3] > 0: # esquerda
            self.rotaciona_esquerda()


    def inferir_cerebro(self):
        if not self.colidiu:
            saidaCerebro = []
            entradaCerebro = self.ler_sensores()

    def update(self, matrizColisao):

        # self.acao = self.cerebro(self.sensores)

        if not self.colidiu:
            leituraSensores = self.ler_sensores(matrizColisao)
            self.cerebro.calcularSaida()
            resCerebro = self.cerebro.copiarDaSaida()

            self.tomarDecisoes(resCerebro)

            self.velocidadeX = - np.cos(np.deg2rad(self.angulo)) * self.velocidade
            self.velocidadeY = np.sin(np.deg2rad(self.angulo)) * self.velocidade

            # Verifica se ocorreu colisao
            if (matrizColisao[self.rect.x + int(self.velocidadeX),
                              self.rect.y + int(self.velocidadeY)]) == 0:
                self.colidiu = True

            elif (matrizColisao[self.rect.x + int(self.velocidadeX), self.rect.y + int(self.velocidadeY)]) == 1:
                # não colidiu, pode mover
                self.rect.x = self.rect.x + int(self.velocidadeX)
                self.rect.y = self.rect.y + int(self.velocidadeY)
