import pygame
from assets.__init__ import sprites_dict

class Bird:
    IMGS = sprites_dict['bird']
    MAX_ROTATION = 30
    MIN_ROTATION = -50
    ROT_VEL = 40
    state_cycle_rate = 5

    def __init__(self, x, y):
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
        return self._x

    @property
    def y(self):
        return self._y
    
    @property
    def rect(self):
        return self._rect

    def jump(self):
        self.vel = 14.5
        self.calculate_new_y()

        self.tilt_up()

    def do_nothing(self):
        self.vel -=1
        self.calculate_new_y()

        self.tilt_down()

    def calculate_new_y(self):
        if self.vel > 12:
            self.vel = 12

        self._y -= self.vel

    def tilt_down(self):
        self.tilt_tick += 1

        if self.tilt_tick > 15:
            self.tilt -= 10
            self.tilt_handler()

    def tilt_up(self):
        self.tilt = 20
        self.tilt_handler()

        self.tilt_tick = 0

    def tilt_handler(self):
        if self.tilt > self.MAX_ROTATION:
            self.tilt = self.MAX_ROTATION
        elif self.tilt < self.MIN_ROTATION:
            self.tilt = self.MIN_ROTATION

    def flap_animation_tick_handler(self):
        if self.tilt == self.MIN_ROTATION:
            self.state = 1
        else:
            self.animation_tick += 1

            if self.animation_tick >= Bird.state_cycle_rate:
                self.cycle_bird_state()
                self.animation_tick = 0


    @staticmethod
    def tilt_bird(image, angle):
        tilted_bird = pygame.transform.rotate(image, angle)

        return tilted_bird

    def cycle_bird_state(self):
        self.state += 1

        if self.state > 2:
            self.state = 0

    def draw(self,win):
        self.flap_animation_tick_handler()

        self._rect = win.blit(self.tilt_bird(self.img[self.state], self.tilt), (self._x, self._y))

    def get_mask(self):
        mask = pygame.mask.from_surface(self.tilt_bird(self.img[self.state], self.tilt))
        return mask