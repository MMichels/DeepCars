import sys
import os
import time
import numpy as np

from random import randint
from typing import List
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import pygame
from pygame.locals import *
import pygame.surfarray as sfarray

from src.cenario import Pista
from src.agentes import Carro, ANGULO_INICIO
from src.camera import Camera
from src.utils import load_image
from src.utils.logDuracao import listaTempos, encontrarMedia

x_window_pos = 15
y_window_pos = 15
os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(x_window_pos, y_window_pos)
QTD_CARROS = 40
TEMPO_PRE_COMPETICAO = 20

def verificarEvento(event):
    camera.verificar_eventos(event)

def limpar_eventos():
    pygame.event.clear()

def posiciona_carros_largada(posicao_faixa: pygame.Rect, carros: List[Carro]):
    for carro in carros:
        bottom_faixa = posicao_faixa.bottom
        left_faixa = posicao_faixa.left
        largura_faixa = posicao_faixa.height
        altura_faixa = posicao_faixa.width

        topo_carro = randint(bottom_faixa, bottom_faixa + 150)
        esquerda_carro = randint(left_faixa + 10, left_faixa + largura_faixa + 20)

        carro.rect.top = topo_carro
        carro.rect.left = esquerda_carro

def inicializaCompeticao(carros):
    Carro.colidirRetardatarios(carros)

def competir(carros: List[Carro], pista: Pista):
    pista.verifica_distancia_corte(carros)

def encerrar_competicao(carros, pista: Pista):
    Carro.calculaFitness(carros, pista.comprimento_pista, pista.matriz_distancias)

def desenha_distancia_corte(screen, pista):
    text = 'Distância de corte: {}'.format(int(pista.distancia_corte))
    text = pista.font.render(text, 1, (200, 200, 200))
    text_pos = text.get_rect(centerx=screen.get_width() / 2, y=0)
    screen.blit(text, text_pos)

atualizandoCenario = False
def attCenario(screen, pista: Pista, faixa_largada, faixa_largada_pos, faixa_chegada, faixa_chegada_pos):
    atualizandoCenario = True
    screen.fill([0, 0, 0])
    pista.clean()
    pista.blit(faixa_largada, faixa_largada_pos)
    pista.blit(faixa_chegada, faixa_chegada_pos)
    atualizandoCenario = False

def salvaMelhorRede(cerebro, fitness):
    melhorDna = cerebro.copiarDNA()
    melhorDna = np.array(melhorDna)
    np.savetxt('./res/DNA/DNA-{}.txt'.format(fitness), melhorDna, '%.10f')

def iniciar_nova_competicao(carros, faixa_largada_pos, pista: Pista):
    Carro.calculaFitness(carros, pista.comprimento_pista, pista.matriz_distancias)
    carros = Carro.realizarMutacao(carros)
    salvaMelhorRede(carros[-1].cerebro, carros[-1].fitness)
    for i in range(len(carros)):
        carros[i].reiniciar()
    posiciona_carros_largada(faixa_largada_pos, carros)
    pista.distancia_corte = pista.comprimento_pista


pygame.init()

screen = pygame.display.set_mode((1300, 700))

font = pygame.font.SysFont('arial', 30)
text = font.render("Inicializando...", 1, (255, 255, 255))
text_rect = text.get_rect(
    centerx=screen.get_width() / 2,
    centery = screen.get_height() / 2
)
screen.blit(text, text_rect)
pygame.display.update()

pista = Pista('pista6')
camera = Camera()

faixa_largada, faixa_largada_pos = load_image('./res/images/faixa.png')
faixa_largada_pos.topleft = 1210, 700

faixa_chegada, faixa_chegada_pos = load_image('./res/images/faixa.png')
faixa_chegada_pos.topleft = 1210, 1040

pista.preencher_matriz_distancias(faixa_chegada_pos)
pista.blit(faixa_largada, faixa_largada_pos)

carros = []
for c in range(QTD_CARROS):
    carros.append(Carro(pista.matriz_colisao, pista.matriz_distancias, faixa_largada_pos))

posiciona_carros_largada(faixa_largada_pos, carros)

renderCarros = pygame.sprite.RenderPlain(carros)

clock = pygame.time.Clock()
inicioPartida = time.time()
competindo = False
Jogando = True
rodada = 0
pista.rect.bottom = 850
pista.rect.right = 1300
while Jogando:
    #print('.', end='')
    ini = time.time()
    clock.tick(60)
    exibeParedesColisao = False
    exibeSensoresMelhorCarro = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Jogando = False
            break
        if event.type in [KEYDOWN, KEYUP]:
            if event.key in [K_DOWN, K_UP, K_RIGHT, K_LEFT]:
                camera.verificar_eventos(event)
            elif event.key == K_z:
                exibeParedesColisao = True
            elif event.key == K_c:
                exibeSensoresMelhorCarro = True
            #carros[0].movimentar_manualmente(event)

    if True in camera.camBtnStates.values():
        pista.rect = camera.mov_cenario(pista.rect)

    if (time.time() - inicioPartida) >= TEMPO_PRE_COMPETICAO and not competindo:
        print('INICIANDO COMPETIÇÃO!!!!')
        inicializaCompeticao(carros)
        competindo = True

    if competindo:
        carrosCompetindo = [c for c in carros if not c.colidiu]
        competir(carrosCompetindo, pista)

        carrosColididos = Carro.contaCarrosColididos(carros)
        if carrosColididos == QTD_CARROS or pista.distancia_corte <= 1:
            print('Duração dessa partida: {} segundos'.format(int(time.time() - inicioPartida)))

            melhorCarro = Carro.buscarMelhorCarro(carros, pista.matriz_distancias, pista.comprimento_pista)

            print('Distancia entre o melhor carro e a faixa de chegada: ',
                  pista.matriz_distancias[melhorCarro.rect.centerx][melhorCarro.rect.centery])

            encerrar_competicao(carros, pista)
            iniciar_nova_competicao(carros, faixa_largada_pos, pista)
            inicioPartida = time.time()
            competindo = False
            rodada += 1
            print('Geração: {}'.format(rodada))


    Thread(target=attCenario, name='tAttCenario', args=(screen, pista, faixa_largada, faixa_largada_pos, faixa_chegada, faixa_chegada_pos)).start()
    # Multi threading atualização dos carros
    #p = ThreadPoolExecutor(os.cpu_count() - 1)
    #with p:
    #    l = p.map(Carro.update, carros)
    #    list(l)

    renderCarros.update()

    while(atualizandoCenario):
        time.sleep(0.0001)

    renderCarros.draw(pista.image)

    if exibeParedesColisao:
        pista.blit(pista.imagemParedesColisao, pista.imagemParedesColisao.get_rect())
    if exibeSensoresMelhorCarro:
        melhorCarro = Carro.buscarMelhorCarro(carros, pista.matriz_distancias, pista.comprimento_pista)
        pista.desenhaSensores(melhorCarro)

    screen.blit(pista.image, pista.rect)

    desenha_distancia_corte(screen, pista)
    pygame.display.update()

    end = time.time()
    listaTempos.append(end - ini)
    #if rodada == 5:
    #    jogando = False
    #    break

print(encontrarMedia())