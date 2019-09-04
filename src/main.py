import sys
import pygame
from pygame.locals import *

from src import Cenario, Camera

pygame.init()

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 860)
screen = pygame.display.set_mode(SCREEN_SIZE)

cenario = Cenario('./res/images/pista.png')
camera = Camera(cenario)

def verify_key_events(ev, btnStates):
    pressed = False

    if ev.type == pygame.KEYDOWN:
        pressed = True
    if ev.key == pygame.K_DOWN:
        btnStates['K_DOWN_PRESSED'] = pressed
    elif ev.key == pygame.K_UP:
        btnStates['K_UP_PRESSED'] = pressed
    elif ev.key == pygame.K_LEFT:
        btnStates['K_LEFT_PRESSED'] = pressed
    elif ev.key == pygame.K_RIGHT:
        btnStates['K_RIGHT_PRESSED'] = pressed

    return btnStates

def mov_cenario(btnStates, backgrndPos):
    if btnStates['K_DOWN_PRESSED']:
        backgrndPos.top -= 4
    if btnStates['K_UP_PRESSED']:
        backgrndPos.top += 4
    if btnStates['K_LEFT_PRESSED']:
        backgrndPos.right -= 4
    if btnStates['K_RIGHT_PRESSED']:
        backgrndPos.right += 4

    return  backgrndPos

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
            camera.camBtnStates = verify_key_events(event, camera.camBtnStates)
        pygame.event.clear()

    if True in camera.camBtnStates.values():
        cenario.position = mov_cenario(camera.camBtnStates, cenario.position)

    screen.blit(cenario.img, cenario.position)
    pygame.display.update()
