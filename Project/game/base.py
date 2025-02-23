import pygame
from assets.__init__ import sprites_dict


class Base:
    BASE_IMG = sprites_dict['base']
    VEL = 5
    width, height = BASE_IMG.get_width(), BASE_IMG.get_height()
    IMG = BASE_IMG


    def __init__(self, x, y):
        self._y = y
        self._x = x
        self._rect = None
        self.IMG = self.IMG.convert()

    @property
    def rect(self):
        return self._rect

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val

    def move(self):
        self._x -= self.VEL

    def draw(self,win):
        self._rect = win.blit(self.IMG, (self._x, self._y))
        