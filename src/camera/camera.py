from pygame.locals import KEYDOWN, KEYUP, K_DOWN, K_UP, K_LEFT, K_RIGHT
import pygame

class Camera:
   
    def __init__(self):
        self.camBtnStates = {
            'K_DOWN_PRESSED': False,
            'K_UP_PRESSED': False,
            'K_LEFT_PRESSED': False,
            'K_RIGHT_PRESSED': False,
        }
        
    def mov_cenario(self, cenario_pos):
        if self.camBtnStates['K_DOWN_PRESSED']:
            cenario_pos.top -= 4
        if self.camBtnStates['K_UP_PRESSED']:
            cenario_pos.top += 4
        if self.camBtnStates['K_LEFT_PRESSED']:
            cenario_pos.right -= 4
        if self.camBtnStates['K_RIGHT_PRESSED']:
            cenario_pos.right += 4
        return cenario_pos

    def verificar_eventos(self, event):
        pressionado = event.type == KEYDOWN

        if event.key in [K_DOWN, K_UP, K_RIGHT, K_LEFT]:
            if event.key == K_DOWN:
                keyCode = 'K_DOWN_PRESSED'
            elif event.key == K_UP:
                keyCode = 'K_UP_PRESSED'
            elif event.key == K_RIGHT:
                keyCode = 'K_RIGHT_PRESSED'
            elif event.key == K_LEFT:
                keyCode = 'K_LEFT_PRESSED'

            self.camBtnStates[keyCode] = pressionado

