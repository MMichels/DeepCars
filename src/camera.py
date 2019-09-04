from pygame.locals import KEYDOWN, KEYUP, K_DOWN, K_UP, K_LEFT, K_RIGHT


class Camera:
   
    def __init__(self, cenario):
        self.camBtnStates = {
            'K_DOWN_PRESSED': False,
            'K_UP_PRESSED': False,
            'K_LEFT_PRESSED': False,
            'K_RIGHT_PRESSED': False,
        }
        
    def mov_cenario(self, cenario_pos):
        if self.camBtnStates['K_DOWN_PRESSED']:
            cenario_pos.top -= 4
        if self.myBrnStates['K_UP_PRESSED']:
            cenario_pos.top += 4
        if self.myBrnStates['K_LEFT_PRESSED']:
            cenario_pos.right -= 4
        if self.myBrnStates['K_RIGHT_PRESSED']:
            cenario_pos.right += 4
        return cenario_pos
