import numpy as np
from numba import jit

MAIOR_DISTANCIA_POSSIVEL = 100000


@jit(nopython=True, cache=True)
def preencher_matriz_colisao(imageArray: np.ndarray, matriz_colisao):
    for w in range(imageArray.shape[0]):
        for h in range(imageArray.shape[1]):
            pixel = imageArray[w, h]
            if pixel[0] == 110 and pixel[1] == 110 and pixel[2] == 110:
                matriz_colisao[w][h] = 1

    return matriz_colisao


@jit(nopython=True)
def preencher_matriz_distancias(imageArray: np.ndarray, matrizColisao: np.ndarray, matrizDistancias: np.ndarray,
                                xyLinhaChegada):
    matrizDistancias[xyLinhaChegada[0]][xyLinhaChegada[1]] = 0
    while True:
        mudanca = 0
        for w in range(imageArray.shape[0]):
            for h in range(imageArray.shape[1]):
                if matrizColisao[w][h] == 1:
                    menor_vizinho = _encontrarMenorVizinho(matrizDistancias, w, h)
                    menor_vizinho += 1
                    if menor_vizinho < matrizDistancias[w][h]:
                        matrizDistancias[w][h] = menor_vizinho
                        mudanca += 1
                else:
                    matrizDistancias[w][h] = -1
        if mudanca == 0:
            break

    return matrizDistancias


@jit(nopython=True, cache=True)
def calcula_comprimento_pista(matriz_distancias, matriz_colisao):
    print('Procurando maior distancia...')
    maior = 0
    for w in range(matriz_distancias.shape[0]):
        for h in range(matriz_distancias.shape[1]):
            if matriz_colisao[w][h] == 1:
                if matriz_distancias[w][h] > maior and matriz_distancias[w][h] != MAIOR_DISTANCIA_POSSIVEL:
                    maior = matriz_distancias[w][h]

    return maior


@jit(nopython=True, cache=True)
def _encontrarMenorVizinho(matrizDistancias: np.ndarray, i, j):
    vizinhos = np.array([
        matrizDistancias[i - 1][j + 1],
        matrizDistancias[i][j + 1],
        matrizDistancias[i + 1][j + 1],
        matrizDistancias[i - 1][j],

        matrizDistancias[i + 1][j],
        matrizDistancias[i - 1][j - 1],
        matrizDistancias[i][j - 1],
        matrizDistancias[i + 1][j + 1]])

    menor = MAIOR_DISTANCIA_POSSIVEL
    for i in vizinhos:
        if menor > i >= 0:
            menor = i

    return menor


@jit(nopython=True, cache=True)
def constroi_paredes_colisao(matrizColisao: np.ndarray, paredesColisao: np.ndarray):
    branco = [255, 255, 255]
    for i in range(matrizColisao.shape[0]):
        for j in range(matrizColisao.shape[1]):
            if matrizColisao[i][j] > 0:
                paredesColisao[i][j] = branco
    return paredesColisao
