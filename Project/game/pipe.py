"""
Flappy bird Pipe class.
Responsible for creating and moving pipes in the game
"""

import pygame, random
import math
from assets.__init__ import sprites_dict

class Pipe:
    """
    A single pipe instance includes the top and bottom pipe for the same x coordinate
    For every instance of the game, there should be 2 pipe class instances
    One rendered in the screen and another outside of the screen waiting to be rendered in once the first base moves out
    And when the pipe moves completely out of the screen, reset the position to the end of the other pipe

    PIPE_IMG contains the loaded pygame sprite for both upper and lower pipes
    VEL controls the amount of pixels the base moves every tick
    GAP controls the distance in pixels between the upper and lower pipe
    INTERVAL controls the distance in pixels between each wave of pipe
    """
    PIPE_IMG = sprites_dict['pipe']
    GAP = 200
    VEL = 5
    INTERVAL = 380

    def __init__(self, x):
        """
        Pipe Class' Constructor

        :param x: type: int
            x coordinates of the pipe in reference to the left corner of the sprite
        """
        self.x = x
        self.height = 0
        self.gap = 100
        
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG

        self.rect_top = pygame.Rect(self.x, self.top, self.PIPE_TOP.get_width(), self.PIPE_TOP.get_height())
        self.rect_bottom = pygame.Rect(self.x, self.bottom, self.PIPE_BOTTOM.get_width(), self.PIPE_BOTTOM.get_height())


        self.passed = False
        self.set_height()

    def set_height(self):
        """
        Sets the pipe height randomly
        """
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

        # Atualiza os retângulos sempre que o tamanho for definido
        self.rect_top.topleft = (self.x, self.top)
        self.rect_bottom.topleft = (self.x, self.bottom)

    @property
    def width(self):
        """
        :return: type: int
            returns the pipe width
        """
        return self.PIPE_TOP.get_width()

    def move(self):
        """
        Moves the pipes towards left of the pygame screen at the rate of velocity set
        """
        self.x -= self.VEL

        self.rect_top.x = self.x
        self.rect_bottom.x = self.x

    def draw(self, win):
        """
        Draws/renders the pipe to the pygame screen

        :param win: type: pygame.surface
            The surface/screen of the game for displaying purposes
        """
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def get_mask(self):
        """
        Extracts the mask from the sprite to provide pixel based collision detection

        :return: type: pygame.mask.Mask
            The extracted mask object
        """
        masks = [pygame.mask.from_surface(pipe) for pipe in [self.PIPE_TOP, self.PIPE_BOTTOM]]

        return masks

    def collide(self, bird):
        """
        Checks if the bird has collided with one of the two pipes.

        Fisrt checks if the rectangles collide then checks if the bird's mask 
        overlaps with any of the pipe's mask and return the point of overlapping or None if there is no overlapping

        The overlaping method can be EXTREMELY costly if used multiple times

        Checks if the bird has hitted the pipe outside the screen
        
        Returns True if Collided 

        :param bird: type: Bird Obj
            List containing the loaded pygame bird state images

        :return: type: boolean
        """

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        bottom_offset = tuple(map(math.ceil, (self.x - bird.x, self.bottom - bird.y)))
        top_offset = tuple(map(math.floor, (self.x - bird.x, self.top - bird.y)))

        if bird.rect.colliderect(self.rect_top) or bird.rect.colliderect(self.rect_bottom):
            b_point = bird_mask.overlap(bottom_mask, bottom_offset)
            t_point = bird_mask.overlap(top_mask, top_offset)

            if t_point or b_point:
                return True
        
        elif bird.y < 0 and self.x < bird.x < (self.x + self.PIPE_TOP.get_width()):
            return True
        
        return False