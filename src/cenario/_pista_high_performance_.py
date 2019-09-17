import numba

import numpy as np
from numba import jit, njit
from numba.typed import List

MAIOR_DISTANCIA_POSSIVEL = 99999999

@jit(nopython=True)
def preencher_matriz_colisao(imageArray: np.ndarray, matriz_colisao):
    for w in range(imageArray.shape[0]):
        for h in range(imageArray.shape[1]):
            pixel = imageArray[w, h]
            if pixel[0] == 110 and pixel[1] == 110 and pixel[2] == 110:
                matriz_colisao[w][h] = 1

    return matriz_colisao


@jit(nopython=True)
def preencher_matriz_distancias(imageArray: np.ndarray, matrizColisao: np.ndarray, matrizDistancias: np.ndarray, xyLinhaChegada):

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
        print('Mudanças: ', mudanca)
        if mudanca == 0:
            break

    for w in range(imageArray.shape[0]):
        for h in range(imageArray.shape[1]):
            if matrizColisao[w][h] == 0:
                matrizDistancias[w][h] = -1
    return matrizDistancias

@jit(nopython=True)
def encontrar_maior_distancia(matriz_distancias, matriz_colisao):
    print('Procurando maior distancia...')
    maior = 0
    for w in range(matriz_distancias.shape[0]):
        for h in range(matriz_distancias.shape[1]):
            if matriz_colisao[w][h] == 1:
                if matriz_distancias[w][h] > maior and matriz_distancias[w][h] != np.inf:
                    maior = matriz_distancias[w][h]

    return maior


@jit(nopython=True)
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
