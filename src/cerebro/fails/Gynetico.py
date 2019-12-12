import numpy as np
from cyrebro import PyDensa

from memory_profiler import profile

DECAIMENTO_MUTACOES = 0.999
MINIMO_MUTACOES = 15
VALOR_PADRAO_PESOS = 10000


class Gynetico(PyDensa):

    def __init__(self, qtdNeuroniosEntrada, qtdCamadasEscondidas, profundidadeEscondidas, qtdNeuroniosSaida):
        super().__init__()
        self.tamDNA = self._calcula_tamanho_DNA()
        self.qtdGenesCamadaSaida = self._calcula_qtd_genes_saida()
        self.qtdGenesCamadasEscondidas = self.tamDNA - self.qtdGenesCamadaSaida
        self.qtdMutacoes = self.tamDNA

    def __call__(self, valorEntrada: list):
        assert len(valorEntrada) == self.qtdNeuroniosEntrada, "A quantidade de valores de entrada nao condiz com o \
                                                              numero de neuronios de entrada"
        self.aplicarEntrada(valorEntrada)
        self.calculaSaida()
        return self.obterSaida()

    def mudar_valor(self, valor, tipoMutancao):
        numero = 0
        if tipoMutancao == 0:
            valor = np.random.uniform(0, VALOR_PADRAO_PESOS + 1, 1)[0]
        elif tipoMutancao == 1:
            numero = np.random.uniform(0, VALOR_PADRAO_PESOS + 1) / VALOR_PADRAO_PESOS + 0.5
            valor *= numero
        elif tipoMutancao == 2:
            numero = np.random.uniform(0, VALOR_PADRAO_PESOS + 1) / (VALOR_PADRAO_PESOS / 10)
            valor += numero
        del numero
        return valor

    @profile(precision=4)
    def mutacao_camadas_escondidas(self, indiceMutacao: int, tipoMutacao: int):
        contador = 0
        indicePeso = -1
        for indiceCamada in range(self.qtdCamadas):
            c = self.camadasEscondidas[indiceCamada]
            for indiceNeuronio in range(c.qtdNeuronios):
                n = c.neuronios[indiceNeuronio]
                if n.qtdLigacoes + contador > indiceMutacao:
                    indicePeso = indiceMutacao - contador
                    break
                else:
                    contador += n.qtdLigacoes
                if indicePeso >= 0:
                    break
            if indicePeso >= 0:
                break
        # Obtem o valor que será alterado
        p = n.pesos
        v = p[indicePeso]
        # altera o valor
        v = self.mudar_valor(v, tipoMutacao)
        p[indicePeso] = v
        # altera os pesos do neuronio
        n.pesos = p

        #altera os neuronios da camada
        ns = c.neuronios
        ns[indiceNeuronio] = n
        c.neuronios = ns
        del ns, n, p, v

        # altera as camadas escondidas
        cs = self.camadasEscondidas
        cs[indiceCamada] = c
        self.camadasEscondidas = cs
        del cs, c, contador, indiceMutacao, indicePeso, indiceNeuronio, indiceCamada

    @profile(precision=4)
    def mutacao_camada_saida(self, indiceMutacao: int, tipoMutacao: int):
        contador = self.qtdGenesCamadasEscondidas
        for indiceNeuronio in range(self.camadaSaida.qtdNeuronios):
            n = self.camadaSaida.neuronios[indiceNeuronio]
            for indicePeso in range(n.qtdLigacoes):
                contador += 1
                if contador >= indiceMutacao:
                    break
            if contador >= indiceMutacao:
                break

        c = self.camadaSaida
        ns = c.neuronios
        n = ns[indiceNeuronio]
        p = n.pesos
        v = p[indicePeso]
        v = self.mudar_valor(v, tipoMutacao)
        p[indicePeso] = v
        n.pesos = p
        ns[indiceNeuronio] = n
        c.neuronios = ns
        self.camadaSaida = c
        del contador,  c, ns, n, p, v, indiceNeuronio, indicePeso, indiceMutacao


    def realiza_mutacao(self, indiceMutacao: int, tipoMutacao: int):
        print(indiceMutacao)
        if indiceMutacao < self.qtdGenesCamadasEscondidas:
            self.mutacao_camadas_escondidas(indiceMutacao, tipoMutacao)
        else:
            self.mutacao_camada_saida(indiceMutacao, tipoMutacao)

    def evoluir(self):
        mutacoes = int(np.random.uniform(0, self.qtdMutacoes, 1)[0])
        for i in range(mutacoes):
            indiceMutacao = int(np.random.uniform(0, self.tamDNA, 1)[0])
            tipoMutacao = int(np.random.uniform(0, 3, 1)[0])
            self.realiza_mutacao(indiceMutacao, tipoMutacao)

        self.qtdMutacoes = self.qtdMutacoes * DECAIMENTO_MUTACOES \
            if self.qtdMutacoes > MINIMO_MUTACOES \
            else MINIMO_MUTACOES
        del mutacoes, indiceMutacao, tipoMutacao

    def _calcula_tamanho_DNA(self):
        tamDNA = 0
        for c in self.camadasEscondidas + [self.camadaSaida, ]:
            for p in c.neuronios:
                tamDNA += p.qtdLigacoes
        return tamDNA

    def _calcula_qtd_genes_saida(self):
        qtdGenes = 0
        for p in self.camadaSaida.neuronios:
            qtdGenes += p.qtdLigacoes
        return qtdGenes

    def copiar(self, inspiracao):
        self.camadaEntrada = inspiracao.camadaEntrada
        self.camadasEscondidas = inspiracao.camadasEscondidas
        self.camadaSaida = inspiracao.camadaSaida
        return self


if __name__ == '__main__':
    rf = Gynetico(18, 1, 6, 4)
    rp = Gynetico.gerarCopiar(rf)
    entrada = np.random.randint(0, 50, 18)

    saidaFilho = rf(entrada)
    saidaPai = rp(entrada)
    rf.evoluir(rp)
    #rp.evoluir(rf)

    saidaPosEvolucao = rf(entrada)
    saidaPaiPosEvolucao = rp(entrada)

    print('Saida do filho: ', saidaFilho)
    print('Saida do pai: ', saidaPai)
    print('Saida do filho apos evolução: ', saidaPosEvolucao)
    print('Saida do pai apos evolução: ', saidaPaiPosEvolucao)
