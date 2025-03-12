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
    """
    Draws/Renders the instaces for the game and update the screen with pygame Update Method

        :param win: type: pygame.surface
            game screen

        :param bird: type: Bird Object
            The Player's Bird

        :param pipes: type: list
            list containing all pipe objects
        
        :param bases: type: list
            list containing all base objects

        :param score: type: Score obj
    """
    
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
    """
    Initializes the basic elements for the game to run:
        Generates the Bird, Bases, Pipes and Score

    :return: type: dictionary
        Dictionary containing all the Elements created.
    """
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
    """
    Controls when and how the Pipes should be moving on the screen

    Each time one pipe passes the end of the screen it gets repositioned for the end of the end again

    :param pipe_list: type: list
        list containing all pipes
    """
    for index, pipe in enumerate(pipe_list, start=0):
        pipe.move()

        if pipe.x + sprites_dict['pipe'].get_width() <= 0:
            pipe.set_height()
            pipe.passed = False
            pipe.x = pipe_list[index-1].x + pipe.INTERVAL

def score_handler(bird, pipes, score):
    """
    Updates the score each time the bird passed a pipe

        :param bird: type: Bird Object
            The Player's Bird

        :param pipes: type: list
            list containing all pipe objects

        :param score: type: Score obj
    """

    for pipe in pipes:
        if bird.x >= (pipe.x + pipe.x) and not pipe.passed:
            score.score += 1
            pipe.passed = True

def base_animation_handler(bases):
    """
    Controls when and how the Bases should be moving on the screen

    Each time one bases passes the end of the screen it gets repositioned for the end of the end again

    :param bases: type: list
        list containing all base objects
    """
    for index, base in enumerate(bases,start=0):
        base.move()

        if base.x + sprites_dict['base'].get_width() <= 0:
            base.x = bases[index-1].x + sprites_dict['base'].get_width()- 5

def check_crash(bird, bases, pipes):
    """
    Checks if the bird has collided with the base or the pipes

    :param bird: type: Bird Object
            The Player's Bird
    
    :param bases: type: list
        list containing all base objects

    :param pipes: type: list
        list containing all pipe objects
    """
    for b_img, base in zip(bird.img, bases):
    
        if base.collide(bird,b_img):
            return True
    

    for pipe in pipes:
        return pipe.collide(bird)

    return False

def gameover_text(win):
    """
    Draws the GAMEOVER Screen

    :param win: type: pygame.surface
        The game screen
    """
    win.blit(sprites_dict['gameover'].convert_alpha(),
             (((WIN_WIDTH / 2)) - (sprites_dict['gameover'].get_width() / 2),
             (WIN_HEIGHT / 2) - (sprites_dict['gameover'].get_height() / 2)))

def startgame_text(win):
        """
        Draws the GAMESTART Screen
        
        :param win: type: pygame.surface
            The game screen
        """
        win.blit(sprites_dict['startgame'].convert_alpha(),
             (((WIN_WIDTH / 2)) - (sprites_dict['startgame'].get_width() / 2),
             (WIN_HEIGHT / 2) - (sprites_dict['startgame'].get_height() / 2)))

def restart():
    """
    Restarts the main game loop
    """
    main()

def handle_gameover(event):
    """
    Checks if the players has pressed any button that should end or restart the game when GAMEOVER

    if True then runs the quit_game() function.

    :params event: type: pygame.event
        The Key(s) the user is pressing
    """
    if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE)):
        quit_game()
        pygame.quit()
        quit()
                        
    if (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
        restart()

def main():
    """
    The main function of the script
        1. Setups game window & clock
        2. Initializes all instances needed for the game
        3. Main game loop
            Reads and handle all players Inputs
            Checks for GAMEOVER
                If True Handler GAMEOVER with quit or restart
            Render the instances on the screen
    """

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

        clock.tick(60)
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
                    handle_gameover(event)
        pygame.display.update() 
    pygame.quit()
    quit()

if __name__ == '__main__':        
    main()