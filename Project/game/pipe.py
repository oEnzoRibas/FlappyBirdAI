import pygame, random
import math
from assets.__init__ import sprites_dict

class Pipe:
    PIPE_IMG = sprites_dict['pipe']
    GAP = 200
    VEL = 5
    INTERVAL = 380

    def __init__(self, x):
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
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

        # Atualiza os retângulos sempre que o tamanho for definido
        self.rect_top.topleft = (self.x, self.top)
        self.rect_bottom.topleft = (self.x, self.bottom)
    
    def move(self):
        self.x -= self.VEL

        # Atualiza a posição dos retângulos quando os canos se movem
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    
    def get_mask(self):
        masks = [pygame.mask.from_surface(pipe) for pipe in [self.PIPE_TOP, self.PIPE_BOTTOM]]

        return masks

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        bottom_offset = tuple(map(math.ceil, (self.x - bird.x, self.bottom - bird.y)))
        top_offset = tuple(map(math.floor, (self.x - bird.x, self.top - bird.y)))

        if bird.rect.colliderect(self.rect_top) or bird.rect.colliderect(self.rect_bottom):
            #checks if the bird's mask overlaps with any of the pipe's mask and 
            # return the point of overlapping or None if there is no overlapping
            b_point = bird_mask.overlap(bottom_mask, bottom_offset)
            t_point = bird_mask.overlap(top_mask, top_offset)

            if t_point or b_point:
                return True
        
        elif bird.y < 0 and self.x < bird.x < (self.x + self.PIPE_TOP.get_width()):
            return True
        
        return False