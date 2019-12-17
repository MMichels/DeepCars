import numpy as np

from numba import jit, int32

TAXA_APRENDIZADO = 0.1
PESO_INI = 1.0
BIAS = 1


#@jit(nopython=True)
def relu(X):
    if X < 0:
        return 0
    elif X < 10000:
        return X
    else:
        return 10000


class Neuronio:

    def __init__(self):
        self.saida = 1
        self.pesos = np.zeros(1, dtype=np.int32)
        self.qtdLigacoes = 0

    def criarNeuronio(self, qtdLigacoes):
        self.qtdLigacoes = qtdLigacoes
        self.pesos = np.empty(self.qtdLigacoes, dtype=np.int32)
        for i in range(len(self.pesos)):
            self.pesos[i] = np.random.standard_normal()


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

    def aplicarEntrada(self, entrada):
        for i, n in enumerate(self.camadaEntrada.neuronios[:-1]):
            n.saida = entrada[i]

    def obterSaida(self):
        saida = []
        for n in self.camadaSaida.neuronios:
            saida.append(n.saida)
        return saida

    def criarRedeNeural(self):
        for c in range(self.qtdCamadasEscondidas):
            for n in range(self.qtdNeuroniosEs):
                if c == 0:
                    self.camadasEscondidas[c].neuronios[n].criarNeuronio(self.qtdNeuroniosIn)
                else:
                    self.camadasEscondidas[c].neuronios[n].criarNeuronio(self.qtdNeuroniosEs)
        for n in range(self.qtdNeuroniosSaida):
            self.camadaSaida.neuronios[n].criarNeuronio(self.qtdNeuroniosEs)

    def copiarVetorParaCamadas(self, vetor: np.ndarray):
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
        vetorPesosRede = np.array([])
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

    def qtdPesosRede(self):
        qtd = 0
        for c in self.camadasEscondidas:
            for n in c.neuronios:
                qtd += n.qtdLigacoes
        for n in self.camadaSaida.neuronios:
            qtd += n.qtdLigacoes
        return qtd

    def calculaSaida(self):
        # Calculo entre as saidas da camada de entrada e a primeira camada escondida
        somaSaidaNeuroniosEntrada = np.sum([n.saida for n in self.camadaEntrada.neuronios])

        for n in self.camadasEscondidas[0].neuronios[:-1]:
            somaDosPesos = np.sum(n.pesos)
            somatorio = np.multiply(somaSaidaNeuroniosEntrada, somaDosPesos)
            n.saida = relu(somatorio)

        # calculo entre as camadas escondidas:
        for k in range(1, self.qtdCamadasEscondidas):
            somaSaidasCamadaAnterior = np.sum([n.saida for n in self.camadasEscondidas[k - 1].neuronios])
            for n in self.camadasEscondidas[k].neuronios[:-1]:
                somaDosPesos = np.sum(n.pesos)
                somatorio = np.multiply(somaSaidasCamadaAnterior, somaDosPesos)
                n.saida = relu(somatorio)

        # CAlculo entre a ultima camada escondida e a camada de saida
        saida = []
        somaSaidasUltimaCamadaEs = np.sum([n.saida for n in self.camadasEscondidas[-1].neuronios])
        for n in self.camadaSaida.neuronios:
            somaDosPesos = np.sum(n.pesos)
            somatorio = np.multiply(somaSaidasUltimaCamadaEs, somaDosPesos)
            n.saida = relu(somatorio)
            saida.append(n.saida)

        return saida


def testeRede():
    r = RedeNeural(18, 6, 1, 4)
    r.criarRedeNeural()


if __name__ == '__main__':
    import time
    import random
    medias = []
    entradas = [random.randint(0, 100) for i in range(19)]
    r = RedeNeural(18, 6, 1, 4)
    r.criarRedeNeural()

    for c in range(1000):
        inicio = time.time()
        r.aplicarEntrada(entradas)
        r.calculaSaida()
        r.obterSaida()
        end = time.time() - inicio
        medias.append(end)


    print(sum(medias) / len(medias))
