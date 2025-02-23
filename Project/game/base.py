import pygame
from assets.__init__ import sprites_dict


class Base:
    BASE_IMG = sprites_dict['base']
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG


    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL


        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

    def collide(self, bird):
        # Bird has crashed at the base
        if bird.rect.bottom >= self.y:
            return True
        return False