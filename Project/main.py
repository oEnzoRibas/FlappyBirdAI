import pygame
import neat
import time
import os
import sys
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


def quit_game():
    sys.exit()

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: {}".format(str(score)), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(),10))

    base.draw(win)

    bird.draw(win)

    pygame.display.update()

def setup_game_window():
    
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    # Define window caption
    pygame.display.set_caption("Flappy-Bird")

    return screen

def init_game_elements():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]

    return {
        "bird": bird,
        "base": base,
        "pipes": pipes
    }

def score_handler(bird, pipes, score):
        add_pipe = False
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

# def base_animation_handler(base_list):

# """
# Moves both base objects simultaneously
# When any one of the base have move beyond the left side of the screen, reset the position of the base back at the
# end of the other base

# :param base_list: type: list
# List containing both bases class instances
# """

# for base in base_list:
#     # Move both bases
#     base.move()

#     # Check if any base has exited the left side of the screen
#     # If true, place base back to the right side
#     if base.x + sprites_dict['base'].get_width() <= 0:
#         base.x = DISPLAY_WIDTH

def check_crash(bird, base, pipes):
    """
    Check if the bird has crashed in any of these ways
    Ways to crash:
        1. Hitting the base
        2. Hitting the pipe (Both upper & lower pipe)
        3. Flying above the screen height and over a pipe

    :param bird: type: game.bird.Bird
    Bird class instance

    :param base: type: list
    List containing both base class instances

    :param pipes: type: list
    List containing both base class instances
    Note: A single pipe object contains 2 pipes, the upper & lower pipe sprite

    :return: type: bool
    Returns True if bird has crashed, else return False
    """

    # Bird has crashed at the base
    if bird.recct.collidelist([item.rect for item in base]) != -1:
        return True

    for pipe in pipes:
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(pipe.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(pipe.PIPE_BOTTOM)

        bottom_offset = tuple(map(math.ceil, (pipe.x - bird.x, pipe.lower_y - bird.y)))
        top_offset = tuple(map(math.floor, (pipe.x - bird.x, pipe.upper_y - bird.y)))

        #checks if the bird's mask overlaps with any of the pipe's mask and 
        # return the point of overlapping or None if there is no overlapping
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        # Check if bird is above the sky limit and in a pipe
        elif bird.y < 0 and pipe.x < bird.x < (pipe.x + pipe.width):
            return True

    return False


def main():

    pygame.init()

    win = setup_game_window()

    clock = pygame.time.Clock()
    
    elements_dict = init_game_elements()

    base = elements_dict["base"]
    pipes = elements_dict["pipes"]
    bird = elements_dict["bird"]

    score = 0

    run = True
    crashed = False
    start = False
    
    while run:
        
        jump = False

        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #ESC Key
                    quit_game()
                
                elif event.key == (pygame.K_SPACE or pygame.K_UP): #Space Key
                    bird.jump()
                    start = True


        


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