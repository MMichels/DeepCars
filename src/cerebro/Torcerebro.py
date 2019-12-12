import torch
import torch.nn as nn
import numpy as np


class Torcerebro(nn.Module):

    def __init__(self, qtdNeuroniosEntrada, qtdCamadas, profundidade, qtdNeuroniosSaida):
        super(Torcerebro, self).__init__()
        self.cEntrada = nn.Linear(qtdNeuroniosEntrada, profundidade)
        self.hidden = []
        for i in range(qtdCamadas):
            self.hidden.append(nn.Linear(profundidade, profundidade))
        self.cSaida = nn.Linear(profundidade, qtdNeuroniosSaida)
        self.relu = nn.ReLU()
        self.eval()
        self.entrada = [0] * qtdNeuroniosEntrada
        self.saida = [0] * qtdNeuroniosSaida
        self.qtdMutacoes = self.tamanhoDNA

    @property
    def tamanhoDNA(self):
        tamanho = 0
        tamanho += self.cEntrada.weight.shape[0] * self.cEntrada.weight.shape[1]
        tamanho += len(self.hidden) * self.hidden[0].weight.shape[0] * self.hidden[0].weight.shape[1]
        tamanho += self.cSaida.weight.shape[0] * self.cSaida.weight.shape[1]
        return tamanho

    def forward(self, x):
        x = torch.Tensor(x)
        saidaAnterior = self.cEntrada(x)
        for i in range(len(self.hidden)):
            relu = self.relu(saidaAnterior)
            saidaAnterior = self.hidden[i](relu)
        relu = self.relu(saidaAnterior)
        ultimaSaida = self.cSaida(relu)
        return self.relu(ultimaSaida)

    def aplicarEntrada(self, entrada):
        self.entrada = torch.Tensor(entrada)

    def calculaSaida(self):
        self.saida = self.forward(self.entrada)

    def obterSaida(self):
        return self.saida

    def mudarValor(self, valor):
        tipoMutacao = np.random.randint(0, 3, 1)[0]
        if tipoMutacao == 0:
            valor = np.random.randn()
        elif tipoMutacao == 1:
            valor *= np.random.uniform(-1, 1.01)
        elif tipoMutacao == 2:
            valor += np.random.uniform(-1, 1.01)
        return valor

    def copiarDNA(self):
        dna = np.array([], np.float)
        pesosIn = self.cEntrada.weight.detach().numpy()
        pesosHidden = np.array([c.weight.detach().numpy() for c in self.hidden])
        pesosOut = self.cSaida.weight.detach().numpy()
        dna = np.append(dna, pesosIn.reshape(pesosIn.size))
        dna = np.append(dna, pesosHidden.reshape(pesosHidden.size))
        dna = np.append(dna, pesosOut.reshape(pesosOut.size))
        return dna

    def colarDNA(self, dna):
        qtdGenesEntrada = self.cEntrada.weight.shape[0] * self.cEntrada.weight.shape[1]
        qtdGenesSaida = self.cSaida.weight.shape[0] * self.cSaida.weight.shape[1]
        qtdGenesEscondidos = len(dna) - (qtdGenesEntrada + qtdGenesSaida)
        genesEntrada = dna[0: qtdGenesEntrada]
        genesEscondidos = dna[qtdGenesEntrada: qtdGenesEntrada + qtdGenesEscondidos]
        genesSaida = dna[qtdGenesEntrada + qtdGenesEscondidos:]

        genesEscondidos = torch.Tensor(genesEscondidos.reshape(
            [len(self.hidden), self.hidden[0].weight.shape[0], self.hidden[0].weight.shape[1]]))

        self.cEntrada.weight = nn.Parameter(torch.Tensor(genesEntrada.reshape(self.cEntrada.weight.shape)))
        self.cSaida.weight = nn.Parameter(torch.Tensor(genesSaida.reshape(self.cSaida.weight.shape)))
        for i in range(genesEscondidos.shape[0]):
            self.hidden[i].weight = nn.Parameter(genesEscondidos[i])

    def alterarDNA(self, dna):
        mutacoes = np.random.randint(0, int(self.qtdMutacoes), 1)[0]
        while (mutacoes >= 0):
            indiceMutacao = np.random.randint(0, int(self.tamanhoDNA), 1)[0]
            valor = dna[indiceMutacao]
            valor = self.mudarValor(valor)
            dna[indiceMutacao] = valor
            mutacoes -= 1
        return dna

    def sofrerMutacao(self):
        dna = self.copiarDNA()
        dna = self.alterarDNA(dna)
        self.colarDNA(dna)

        if self.qtdMutacoes > (self.qtdMutacoes * 0.15):
            self.qtdMutacoes = self.qtdMutacoes * 0.998

    def copiarRede(self, inpiracao):
        dna = inpiracao.copiarDNA()
        self.colarDNA(dna)


if __name__ == '__main__':
    import time

    rede = Torcerebro(18, 1, 6, 4)

    testeDesempenho = False
    if testeDesempenho:

        entradas = torch.randn(18)
        medias = []
        for i in range(1000):
            ini = time.time()
            rede.aplicarEntrada(entradas)
            rede.calculaSaida()
            rede.obterSaida()
            end = time.time()
            medias.append(end - ini)
        print(sum(medias) / len(medias))

    rede.aplicarEntrada(torch.randn(18))
    rede.calculaSaida()
    print(rede.obterSaida())

    rede.sofrerMutacao()

    rede.calculaSaida()
    print(rede.obterSaida())
