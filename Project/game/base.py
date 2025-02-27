import pygame
from assets.__init__ import sprites_dict


class Base:
    """
    Every instance of the game should have 2 Base class instances
    One rendered in the screen and another outside of the screen waiting to be rendered in once the first base moves out
    And when the base moves completely out of the screen, reset the position to the end of the other base

    velocity controls the amount of pixels the base moves every tick
    image contains the loaded base pygame sprite object
    width and height contains the sprite width and height in pixels
    """
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

    def collide(self,bird,bird_img):
        """
        Checks if the bird has collided with one of the two bases.
        
        Returns True if Collided 

        :param bird: type: Bird Obj
        List containing the loaded pygame bird state images

        :param bird_img: type: pygame.Surface
        pygame sprite of the bird

        :return: type: boolean
        """
        if bird.y + bird_img.get_height() >= self._y:
            return True
        
    def move(self):
        """
        Moves the base towards left of the pygame screen at the rate of velocity set
        """
        self._x -= self.VEL

    def draw(self,win):
        """
        Draws/renders the base to the pygame screen

        :param win: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        self._rect = win.blit(self.IMG, (self._x, self._y))
        