import pygame
import neat
import time
import os
import random
from assets.__init__ import sprites_dict
from game.bird import Bird
from game.pipe import Pipe
from game.base import Base
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = sprites_dict['bird']

PIPE_IMG = sprites_dict['pipe']
BASE_IMG = sprites_dict['base']
BG_IMG = sprites_dict['bg-day']

STAT_FONT = pygame.font.SysFont("comicsans",50)

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: {}".format(str(score)), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(),10))

    base.draw(win)

    bird.draw(win)

    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]

    score = 0

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        
        #bird.move()
        add_pipe = False
        base.move()
        rem = [] 
        for pipe in pipes:
            if pipe.collide(bird):
                #pygame.quit()
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(630))

        for r in rem:
            pipes.remove(r)
        
        if bird.y + bird.img.get_height()>= 730:
            print("A")
            pass

        draw_window(win,bird, pipes, base, score)
 
    pygame.quit()
    quit()

main()