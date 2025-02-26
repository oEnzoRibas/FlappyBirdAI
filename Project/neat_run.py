import pygame
import sys
import os
import math
import neat
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
    birds = []
    base1 = Base(0, WIN_HEIGHT - Base.height + 200)
    base2 = Base(Base.width, WIN_HEIGHT- Base.height + 200)
    pipe1 = Pipe(700)
    pipe2 = Pipe(pipe1.x + Pipe.INTERVAL)
    score = Score()
    

    return {
        "birds": birds,
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
                return True

def base_animation_handler(bases):
    for index, base in enumerate(bases,start=0):
        base.move()

        if base.x + sprites_dict['base'].get_width() <= 0:
            base.x = bases[index-1].x + sprites_dict['base'].get_width()- 5

def check_crash(bird, bases, pipes):   
    for b_img, base in zip(bird.img, bases):
            if base.collide(bird,b_img):
                return True

    for pipe in pipes:
            if pipe.collide(bird):
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

def handle_gameover(event):
    if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE)):
        quit_game()
        pygame.quit()
        quit()
                        
def handle_restart(event):
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
        restart()

def main(genomes, config):
    pygame.init()

    win = setup_game_window()

    clock = pygame.time.Clock()
    
    elements_dict = init_game_elements()

    bases = elements_dict["bases"]
    pipes = elements_dict["pipes"]
    birds = elements_dict["birds"]
    score = elements_dict['score']

    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    run = True
    crashed = False
    start = False
    
    while run:
        
        jump = False

        clock.tick(30)
        
        for event in pygame.event.get():
            handle_gameover(event)

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for index, bird in enumerate(birds):
            start = True
            ge[index].fitness += 0.01

            output = nets[index].activate((bird.y,
                                            abs(bird.y - pipes[pipe_ind].height),
                                                abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:    
                jump = True
                bird.do_nothing()
                

    
        if not crashed:

            win.blit(sprites_dict["bg-day"].convert(), (0, 0))

            if start:

                for index, bird in enumerate(birds):
                    draw_window(win, bird, pipes, bases, score)
                    pipes_animation_handler(pipes)
                    base_animation_handler(bases)
                    #print(f"index {index} bird {bird}")

                    if jump:
                        bird.do_nothing()
                        bird.jump()

                    else: bird.do_nothing()

                    if check_crash(bird,bases,pipes):
                        ge[index].fitness -= 1
                        birds.pop(index)
                        nets.pop(index)
                        ge.pop(index)
                        #crashed = True

                    if score_handler(bird,pipes,score):
                        for g in ge:
                            g.fitness += 2
                        birds.pop(index)
                        nets.pop(index)
                        ge.pop(index)


            else: startgame_text(win)
        else:
            while crashed:
                gameover_text(win)
                pygame.display.update()
                
                for event in pygame.event.get():
                    handle_gameover(event)
                    handle_restart(event)

        #pygame.display.update() 

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat.config.txt")
    run(config_path)