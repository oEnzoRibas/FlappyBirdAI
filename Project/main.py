import pygame
import sys
import math
from assets.__init__ import sprites_dict
from game.bird import Bird
from game.pipe import Pipe
from game.base import Base
from game.score import Score
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = sprites_dict['bird']
PIPE_IMG = sprites_dict['pipe']
BASE_IMG = sprites_dict['base']
BG_IMG = sprites_dict['bg-night']

STAT_FONT = pygame.font.SysFont("comicsans",50)


def quit_game():
    sys.exit()

def draw_window(win, bird, pipes, bases, score):
    
    bg = "bg-night" if score.score % 50 == 0 and score.score > 0 else "bg-day"
    win.blit(sprites_dict[bg], (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
   
    for base in bases:
        base.draw(win)

    bird.draw(win)

    score.draw(win)

    pygame.display.update()

def setup_game_window():
    
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    # Define window caption
    pygame.display.set_caption("Flappy-Bird")

    return screen

def init_game_elements():
    bird = Bird(230,350)
    base1 = Base(0, WIN_HEIGHT - Base.height + 200)
    base2 = Base(Base.width, WIN_HEIGHT- Base.height + 200)
    pipe1 = Pipe(700)
    pipe2 = Pipe(pipe1.x + Pipe.INTERVAL)
    score = Score()
    

    return {
        "bird": bird,
        "bases": [base1,base2],
        "pipes": [pipe1,pipe2],
        "score": score
    }

def pipes_animation_handler(pipe_list):
    for index, pipe in enumerate(pipe_list, start=0):
        pipe.move()

        if pipe.x + sprites_dict['pipe'].get_width() <= 0:
            pipe.set_height()
            pipe.passed = False
            pipe.x = pipe_list[index-1].x + pipe.INTERVAL

def score_handler(bird, pipes, score):
        for pipe in pipes:
            if bird.x >= (pipe.x + pipe.x) and not pipe.passed:
                score.score += 1
                pipe.passed = True

def base_animation_handler(bases):
    for index, base in enumerate(bases,start=0):
        base.move()

        if base.x + sprites_dict['base'].get_width() <= 0:
            base.x = bases[index-1].x + sprites_dict['base'].get_width()- 5

def check_crash(bird, bases, pipes):
    for b, base in zip(bird.img, bases):
    
        if bird.y + b.get_height() >= base._y:
            return True
    

    for pipe in pipes:
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(pipe.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(pipe.PIPE_BOTTOM)

        bottom_offset = tuple(map(math.ceil, (pipe.x - bird.x, pipe.bottom - bird.y)))
        top_offset = tuple(map(math.floor, (pipe.x - bird.x, pipe.top - bird.y)))

        #checks if the bird's mask overlaps with any of the pipe's mask and 
        # return the point of overlapping or None if there is no overlapping
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        elif bird.y < 0 and pipe.x < bird.x < (pipe.x + pipe.x):
            return True

    return False

def gameover_text(win):
    win.blit(sprites_dict['gameover'].convert_alpha(),
             (((WIN_WIDTH / 2)) - (sprites_dict['gameover'].get_width() / 2),
             (WIN_HEIGHT / 2) - (sprites_dict['gameover'].get_height() / 2)))

def startgame_text(win):
        win.blit(sprites_dict['startgame'].convert_alpha(),
             (((WIN_WIDTH / 2)) - (sprites_dict['startgame'].get_width() / 2),
             (WIN_HEIGHT / 2) - (sprites_dict['startgame'].get_height() / 2)))

def restart():
    main()
    print("ASD")
    

def main():

    pygame.init()

    win = setup_game_window()

    clock = pygame.time.Clock()
    
    elements_dict = init_game_elements()

    bases = elements_dict["bases"]
    pipes = elements_dict["pipes"]
    bird = elements_dict["bird"]
    score = elements_dict['score']

    run = True
    crashed = False
    start = False
    
    while run:
        
        jump = False

        clock.tick(40)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #ESC Key
                    quit_game()
                
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP: #Space Key or UP Arrow
                    jump = True
                    start = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:#Left Mouse Button
                    jump = True
                    start = True
                

    
        if not crashed:

            win.blit(sprites_dict["bg-day"].convert(), (0, 0))

            if start:

                draw_window(win, bird, pipes, bases, score)
                pipes_animation_handler(pipes)
                base_animation_handler(bases)

                if jump:
                    bird.jump()

                else: bird.do_nothing()

                score_handler(bird,pipes,score)

                if check_crash(bird,bases,pipes):
                    crashed = True

            else: startgame_text(win)
        else:
            while crashed:
                gameover_text(win)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: #ESC Key
                            quit_game()
                        
                        elif event.key == pygame.K_r: #r Key
                            restart()
        
        pygame.display.update() 
    pygame.quit()
    quit()

if __name__ == '__main__':        
    main()