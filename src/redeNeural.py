import math
import random
import time

import numpy as np

TAXA_APRENDIZADO = 0.1
PESO_INI = 1.0
BIAS = 1


def relu(X):
    if X < 0:
        return 0
    elif X < 10000:
        return X
    else:
        return 10000


def reluDx(X):
    if X < 0:
        return 0
    else:
        return 1


class Neuronio:
    def __init__(self):
        self.erro = 0.0
        self.saida = 1.0
        self._valor_ = 0
        self.pesos = []
        self.qtdLigacoes = 0

    def criarNeuronio(self, qtdLigacoes):
        self.qtdLigacoes = qtdLigacoes
        self.pesos = np.zeros(self.qtdLigacoes)

        for i in range(self.qtdLigacoes):
            random = np.random.uniform(0, 1, 1)[0]
            if random <= 0.5:
                self.pesos[i] = np.random.uniform(size=1)[0]
            else:
                self.pesos[i] = - np.random.uniform(size=1)[0]


class Camada:
    def __init__(self, qtdNeuronios):
        self.qtdNeuronios = qtdNeuronios
        self.neuronios = [Neuronio() for i in range(self.qtdNeuronios)]


class RedeNeural:
    def __init__(self, qtdNeuroniosEntrada, qtdNeuroniosEscondidos, qtdCamadasEscondidas, qtdNeuroniosSaida):
        self.qtdNeuroniosIn = qtdNeuroniosEntrada + BIAS
        self.qtdNeuroniosEs = qtdNeuroniosEscondidos + BIAS
        self.qtdCamadasEscondidas = qtdCamadasEscondidas
        self.qtdNeuroniosSaida = qtdNeuroniosSaida

        self.camadaEntrada = Camada(self.qtdNeuroniosIn)
        self.camadasEscondidas = [Camada(self.qtdNeuroniosEs) for i in range(self.qtdCamadasEscondidas)]
        self.camadaSaida = Camada(self.qtdNeuroniosSaida)

    def criarRedeNeural(self):
        for c in range(self.qtdCamadasEscondidas):
            for n in range(self.qtdNeuroniosEs):
                if c == 0:
                    self.camadasEscondidas[c].neuronios[n].criarNeuronio(self.qtdNeuroniosIn)
                else:
                    self.camadasEscondidas[c].neuronios[n].criarNeuronio(self.qtdNeuroniosEs)
        for n in range(self.qtdNeuroniosSaida):
            self.camadaSaida.neuronios[n].criarNeuronio(self.qtdNeuroniosEs)


    def copiarVetorParaCamadas(self, vetor):
        v = 0

        # copia para as camadas escondidas
        for c in range(self.qtdCamadasEscondidas):
            for n in range(self.camadasEscondidas[c].qtdNeuronios):
                for p in range(self.camadasEscondidas[c].neuronios[n].qtdLigacoes):
                    self.camadasEscondidas[c].neuronios[n].pesos[p] = vetor[v]
                    v += 1

        # Copia para a saida
        for n in range(self.camadaSaida.qtdNeuronios):
            for p in range(self.camadaSaida.neuronios[n].qtdLigacoes):
                self.camadaSaida.neuronios[n].pesos[p] = vetor[v]
                v += 1

    def copiarCamadasParaVetor(self):
        vetorPesosRede = []
        v = 0

        # copia das camadas escondidas
        for c in range(self.qtdCamadasEscondidas):
            for n in range(self.camadasEscondidas[c].qtdNeuronios):
                for p in range(self.camadasEscondidas[c].neuronios[n].qtdLigacoes):
                    vetorPesosRede.append(self.camadasEscondidas[c].neuronios[n].pesos[p])
                    v += 1

        # Copia da saida
        for n in range(self.camadaSaida.qtdNeuronios):
            for p in range(self.camadaSaida.neuronios[n].qtdLigacoes):
                vetorPesosRede.append(self.camadaSaida.neuronios[n].pesos[p])

        return vetorPesosRede

    def copiarParaEntrada(self, valoresEntrada):
        for i, n in enumerate(self.camadaEntrada.neuronios):
            n.saida = valoresEntrada[i]

    def copiarDaSaida(self):
        return [n.saida for n in self.camadaSaida.neuronios]

    def qtdPesosRede(self):
        qtd = 0
        for c in self.camadasEscondidas:
            for n in c.neuronios:
                qtd += n.qtdLigacoes
        for n in self.camadaSaida.neuronios:
            qtd += n.qtdLigacoes
        return qtd

    def calcularSaida(self):
        # Calculo entre as saidas da camada de entrada e a primeira camada escondida
        for i in range(self.camadasEscondidas[0].qtdNeuronios - BIAS):
            somatorio = 0
            for j in range(self.camadaEntrada.qtdNeuronios):
                somatorio += self.camadaEntrada.neuronios[j].saida * self.camadasEscondidas[0].neuronios[i].pesos[j]
            self.camadasEscondidas[0].neuronios[i].saida = relu(somatorio)

        # calculo entre as camadas escondidas:
        for k in range(1, self.qtdCamadasEscondidas):
            for i in range(self.camadasEscondidas[k].qtdNeuronios - BIAS):
                somatorio = 0
                for j in range(self.camadasEscondidas[k - 1].qtdNeuronios):
                    somatorio += self.camadasEscondidas[k - 1].neuronios[j].saida * \
                                 self.camadasEscondidas[k].neuronios[i].pesos[j]
                self.camadasEscondidas[k].neuronios[i].saida = relu(somatorio)

        # CAlculo entre a ultima camada escondida e a camada de saida
        for i in range(self.camadaSaida.qtdNeuronios):
            somatorio = 0
            for j in range(self.camadasEscondidas[-1].qtdNeuronios):
                somatorio += self.camadasEscondidas[-1].neuronios[j].saida * self.camadaSaida.neuronios[i].pesos[j]
            self.camadaSaida.neuronios[i].saida = relu(somatorio)

