"""
Flappy Bird Bird Class
Responsible for creating the Bird Object for the game
"""

import pygame
from assets.__init__ import sprites_dict

class Bird:
    """
    For every instance of the game, there should be 1 bird class instance
    The only exception is in the neat_run script where multiple bird class instances are created to perform parallel
    training

    IMGS contains the loaded bird pygame sprite object
    state_cycle_rate is the amount of ticks passed before switching a different flapping state
    MAX_ROTATION is the maximum angle of tilt allowed for the bird when it is flapping up (Calculated from normal state)
    MIN_ROTATION is the maximum angle of tilt allowed for the bird when it is nose diving down (Calculated from normal state)
    """
    IMGS = sprites_dict['bird']
    MAX_ROTATION = 30
    MIN_ROTATION = -50
    ROT_VEL = 40
    state_cycle_rate = 5

    def __init__(self, x, y):
        """
        Bird Class' Constructor

        :param x: type: int
            the x position for the bird in reference to the left corner of the sprite
        
        :param y: type: int
            the y position for the bird in reference to the left corner of the sprite
        """
        self._x = x
        self._y = y
        self.state = 0
        self.animation_tick = 0
        self.tilt_tick = 0
        self.tilt = 0
        self.vel = 0
        self._rect = None
        self.height = self._y
        self.img_count = 0
        self.img = [bird.convert_alpha() for bird in self.IMGS]
    
    @property
    def x(self):
        """
        Gets the x coordenate
        """
        return self._x

    @property
    def y(self):
        """
        Gets the y coordenate
        """
        return self._y
    
    @property
    def rect(self):
        return self._rect

    def jump(self):
        """
        Simulates the jumping/flapping of the bird by increasing its velocity and tilting the bird
        """
        self.vel = 19.5
        self.calculate_new_y()

        self.tilt_up()

    def do_nothing(self):
        """
        Simulates gravity and angle of fall to the bird when it's not jumping
        """
        self.vel -=1
        self.calculate_new_y()

        self.tilt_down()

    def calculate_new_y(self):
        """
        Calculates and updates the new y coordinate based on the velocity and the current bird position
        """
        if self.vel > 12:
            self.vel = 12

        self._y -= self.vel

    def tilt_down(self):
        """
        Increment the tilt_tick until passing a threshold to actually tilt the bird downwards. 
        Then tilts the bird down incrementally until it reaches the min_tilt value.
        """
        self.tilt_tick += 1

        if self.tilt_tick > 15:
            self.tilt -= 10
            self.tilt_handler()

    def tilt_up(self):
        """
        Tilt the bird up a fixed angle. Multiple calls of this function can stack additively and
        resets the tilt_tick to provide tilt immunity to the bird
        """
        self.tilt = 20
        self.tilt_handler()

        self.tilt_tick = 0

    def tilt_handler(self):
        """
        Ensures that the tilt angle does not pass between the min_tilt & max_tilt thresholds.
        If passed, set the tilt angle back to the min or max respectively
        """
        if self.tilt > self.MAX_ROTATION:
            self.tilt = self.MAX_ROTATION
        elif self.tilt < self.MIN_ROTATION:
            self.tilt = self.MIN_ROTATION

    def flap_animation_tick_handler(self):
        """
        Sets the gliding animation state for when the bird is at a nose dive position tilt
        Otherwise, increment the animation_tick until it reaches a threshold. Once passing the threshold, cycle the
        bird state to simulate bird flapping animation
        """
        if self.tilt == self.MIN_ROTATION:
            self.state = 1
        else:
            self.animation_tick += 1

            if self.animation_tick >= Bird.state_cycle_rate:
                self.cycle_bird_state()
                self.animation_tick = 0

    @property
    def width(self):
        """
        Gets the bird sprite width
        """
        return self.img[self.state].get_width()

    @staticmethod
    def tilt_bird(image, angle):
        """
        Rotates the pygame sprite according to the provided angle and returns the rotated sprite.

        :param image: type: list
            List containing the loaded pygame bird state images

        :param angle: type: int
            Angle of tilt for the bird

        :return: type: pygame.Surface
            pygame sprite of the tilted bird
        """
        tilted_bird = pygame.transform.rotate(image, angle)

        return tilted_bird

    def cycle_bird_state(self):
        """
        Cycles the bird animation state between 0 to 2
        """
        self.state += 1

        if self.state > 2:
            self.state = 0

    def draw(self, win):
        """
        Draws/renders the bird to the pygame screen

        :param win: type: pygame.surface
            The surface/screen of the game for displaying purposes
        """
        self.flap_animation_tick_handler()

        self._rect = win.blit(self.tilt_bird(self.img[self.state], self.tilt), (self._x, self._y))

    def get_mask(self):
        """
        Extracts the mask from the sprite to provide pixel based collision detection

        :return: type: pygame.mask.Mask
            The extracted mask object
        """
        mask = pygame.mask.from_surface(self.tilt_bird(self.img[self.state], self.tilt))
        return mask