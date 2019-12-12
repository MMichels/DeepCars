import pandas as pd

listaTempos = []


def gravarTempos(arquivo):
    dados = pd.DataFrame({'tempos': listaTempos})
    dados.to_csv(arquivo)


def lerTempos(arquivo):
    dados = pd.read_csv(arquivo)
    listaTempos = dados['tempos']


def encontrarMedia():
    dados = pd.DataFrame({'tempos': listaTempos})
    return dados['tempos'].min(),  dados['tempos'].mean(), dados['tempos'].max()