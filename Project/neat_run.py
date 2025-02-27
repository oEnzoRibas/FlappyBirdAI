import pygame
import sys
import os
import math
import neat
import pickle
import visualize
from assets.__init__ import sprites_dict
from visualize import plot_fitness_graph
import matplotlib as plt
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

def startgame_text(win):
        win.blit(sprites_dict['startgame'].convert_alpha(),
             (((WIN_WIDTH / 2)) - (sprites_dict['startgame'].get_width() / 2),
             (WIN_HEIGHT / 2) - (sprites_dict['startgame'].get_height() / 2)))       

def gameover_text(win):
    win.blit(sprites_dict['gameover'].convert_alpha(),
             (((WIN_WIDTH / 2)) - (sprites_dict['gameover'].get_width() / 2),
             (WIN_HEIGHT / 2) - (sprites_dict['gameover'].get_height() / 2)))         
    
def quit_game():
    sys.exit()

def handle_quit(event):
    if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE)):
        quit_game()
        pygame.quit()
        quit()

def restart():
    fitness()

def handle_restart(event):
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
        restart()

def draw_window(win, birds, pipes, bases, score, bird_counter, geneation_counter):
    
    bg = "bg-night" if score.score % 50 == 0 and score.score > 0 else "bg-day"
    win.blit(sprites_dict[bg], (0,0))
    
    for pipe in pipes:
        pipe.draw(win)
   
    for base in bases:
        base.draw(win)

    for bird in (birds):
        bird.draw(win)

    score.draw(win)

    bird_counter = pygame.font.SysFont("arialbd", 36).render("Birds: {}".format(len(birds)), True, (255, 255, 255))
    win.blit(bird_counter, (10, 10))

    generation_counter = pygame.font.SysFont("arialbd", 36).render("Gen: {}".format(population.generation), True, (255, 255, 255))
    win.blit(generation_counter, (10, 35))

    pygame.display.update()

def setup_game_window():
    
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    # Define window caption
    pygame.display.set_caption("Flappy-Bird")

    return screen

def init_game_elements(genomes):
    birds_list = []
    networks_list = []
    genomes_list = []

    for genome_id, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks_list.append(network)

        birds_list.append(Bird((WIN_WIDTH / 2), WIN_HEIGHT / 2))
        
        genome.fitness = 0
        genomes_list.append((genome_id, genome))

    base1 = Base(0, WIN_HEIGHT - Base.height + 200)
    base2 = Base(Base.width, WIN_HEIGHT- Base.height + 200)

    pipe1 = Pipe(700)
    pipe2 = Pipe(pipe1.x + Pipe.INTERVAL)

    score = Score()

    font = pygame.font.SysFont("arialbd", 16)
    bird_counter = font.render("Bird Counter", True, (255, 255, 255))
    generation_counter = font.render("Gen Counter", True, (225, 255, 255))

    return {
        "birds": birds_list,
        "bases": [base1,base2],
        "pipes": [pipe1,pipe2],
        "score": score,
        "networks": networks_list,
        "genomes": genomes_list,
        "bird_counter": bird_counter,
        "generation_counter": generation_counter
    }

def pipes_animation_handler(pipe_list):
    for index, pipe in enumerate(pipe_list, start=0):
        pipe.move()

        if pipe.x + sprites_dict['pipe'].get_width() <= 0:
            pipe.set_height()
            pipe.passed = False
            pipe.x = pipe_list[index-1].x + pipe.INTERVAL

def base_animation_handler(bases):
    for index, base in enumerate(bases,start=0):
        base.move()

        if base.x + sprites_dict['base'].get_width() <= 0:
            base.x = bases[index-1].x + sprites_dict['base'].get_width()- 5
            
def get_closest_pipe_index(bird, pipes):
    """
    Retorna o índice do cano mais próximo que está à frente do pássaro.
    Garante que só muda quando o pássaro ultrapassa completamente o cano.
    """
    closest_index = None
    min_distance = float('inf')

    for i, pipe in enumerate(pipes):
        pipe_right_edge = pipe.x + pipe.PIPE_TOP.get_width()  # Considerando a largura do cano
        distance = pipe_right_edge - bird.x  # Distância até o final do cano

        if distance > 0 and distance < min_distance:  # Apenas canos à frente do pássaro
            min_distance = distance
            closest_index = i

    #print(f"Closest Pipe Index: {closest_index}, Bird X: {bird.x}")  # Debugging
    return closest_index

def score_handler(birds, pipes, score, pipe, genomes):
    """
    Atualiza a pontuação dos pássaros ao passarem pelos canos.
    Aumenta a fitness dos genomas correspondentes.
    """
    
    
    if not check_generation_crash(birds): 
        for i, bird in enumerate(birds):
            pipe_index = get_closest_pipe_index(bird, pipes)

            if pipe_index is not None:
                pipe = pipes[pipe_index]
                #print(f"bird x: {bird.x} pipe x: {pipe.x + pipe.width}")
                if bird.x >= (pipe.x + pipe.width - 5) and not pipe.passed:
                    #print("passed")
                    score.score += 1
                    pipe.passed = True

                    for genome_id, genome in genomes:
                        genome.fitness += 5 

def check_crash(game_elements_dict):   
    """
    Verifica colisões entre os pássaros e os elementos do jogo (bases e canos).
    Remove pássaros que colidirem e penaliza seus genomas.
    """

    birds = game_elements_dict['birds']
    pipes = game_elements_dict['pipes']
    bases = game_elements_dict['bases']
    genomes = game_elements_dict['genomes']
    networks = game_elements_dict['networks']

    to_remove = []

    for index in range(len(birds) - 1, -1, -1):
        bird = birds[index]
        genome = genomes[index][1]

        if any(bird.rect.colliderect(base.rect) for base in bases):
            genome.fitness -= 10
            to_remove.append(index)
            continue

        closest_pipe = min(
            (pipe for pipe in pipes if pipe.rect_top.right > bird.rect.left),
            key=lambda p: p.rect_top.right - bird.rect.left,
            default=None
        )

        if closest_pipe:
           
            if bird.rect.colliderect(closest_pipe.rect_top) or bird.rect.colliderect(closest_pipe.rect_bottom):
                
                if bird.get_mask().overlap(closest_pipe.get_mask()[0], (closest_pipe.x - bird.x, closest_pipe.top - bird.y)) or \
                   bird.get_mask().overlap(closest_pipe.get_mask()[1], (closest_pipe.x - bird.x, closest_pipe.bottom - bird.y)):
                    genome.fitness -= 1
                    to_remove.append(index)
                    continue

        if bird.y < 0:
            genome.fitness -= 10
            to_remove.append(index)

    for index in to_remove:
        del birds[index]
        del genomes[index]
        del networks[index]

def check_generation_crash(birds):
    if len(birds) == 0:
        return True
    else: return False        
                        
def fitness(genomes, config):
    pygame.init()

    win = setup_game_window()

    clock = pygame.time.Clock()
    
    elements_dict = init_game_elements(genomes)

    bases = elements_dict["bases"]
    pipes = elements_dict["pipes"]
    birds = elements_dict["birds"]
    score = elements_dict['score']
    networks = elements_dict["networks"]
    genomes = elements_dict["genomes"]
    bird_counter = elements_dict["bird_counter"]
    generation_counter = elements_dict["generation_counter"]

    run = True
    crashed = False
    
    while run:

        clock.tick(60)
        
        for event in pygame.event.get():
            handle_quit(event)

        if not crashed:

            win.blit(sprites_dict["bg-day"].convert(), (0, 0))
            
            draw_window(win, birds, pipes, bases, score, bird_counter, generation_counter)
            pipes_animation_handler(pipes)
            base_animation_handler(bases)

            for index, bird in enumerate(birds):
                #print(f"index {index} bird {bird}")

                genomes[index][1].fitness += 0.1
            
                pipe_index = get_closest_pipe_index(bird, pipes)
                bird_height = (bird.y)
                pipe_top_height = (pipes[pipe_index].top)
                pipe_bottom_height = (pipes[pipe_index].bottom)
                #print(f"pipe index: {pipe_index}")

                # passing to the model the bird location, pipes location
                output = networks[index].activate(((bird_height),
                                                abs(bird_height - pipe_top_height),
                                                abs(bird_height - pipe_bottom_height)))
            
                if output[0] > 0.5:    
                    bird.jump()
                else:
                    bird.do_nothing()

            check_crash(elements_dict)

            score_handler(birds,pipes,score, pipe_index, genomes)

            if check_generation_crash(birds):
                crashed = True

            if score.score > 1000:
                print("score limit reached, skipping generation")
                break

        else:
            pygame.quit()
            break

        pygame.display.update() 

if __name__ == '__main__':
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat.config.txt")

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    # Create population
    population = neat.Population(config)

    # Initialize stats reporter
    population.add_reporter(neat.StdOutReporter(True))
    statistics = neat.StatisticsReporter()
    population.add_reporter(statistics)

    # Run fitness function
    population.run(fitness, 50)

    # Get best genome and save it
    winner = statistics.best_genome()

    # Save best model
    print("Saving model...")
    with open(os.path.join("models/", "winner-{:.0f}.pkl".format(winner.fitness)), 'wb') as data:
        pickle.dump(winner, data, protocol=pickle.HIGHEST_PROTOCOL)

    # Visualize fitness graph
    print("Saving fitness graph...")
    plot_fitness_graph(statistics)



