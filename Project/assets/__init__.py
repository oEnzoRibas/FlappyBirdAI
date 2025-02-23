import copy, os, pygame

pygame.init()

ASSET_PATH = "Project/assets"

sprites_dict = {
    "nums": [
        "sprites/nums/0.png",
        "sprites/nums/1.png",
        "sprites/nums/2.png",
        "sprites/nums/3.png",
        "sprites/nums/4.png",
        "sprites/nums/5.png",
        "sprites/nums/6.png",
        "sprites/nums/7.png",
        "sprites/nums/8.png",
        "sprites/nums/9.png"
    ],
    
    "gameover": "sprites/messages/gameover.png",
    "startgame": "sprites/messages/startgame.png",

    "bg-day": "sprites/background/bg_day.png",
    "bg-night": "sprites/background/bg_night.png",

    "base": "sprites/base/base.png",

    "bird": [
        "sprites/bird/bird1.png",
        "sprites/bird/bird2.png",
        "sprites/bird/bird3.png"
    ],

    "pipe": "sprites/pipe/pipe.png"
}

def scale_image(image, scale_factor):
    width, height = image.get_size()
    return pygame.transform.scale(image, (int(width * scale_factor), int(height * scale_factor)))

SCALE_FACTOR = 2

for key, value in copy.deepcopy(sprites_dict).items():
    if isinstance(value, list):
        for index, value in enumerate(value):
            image = pygame.image.load(os.path.join(ASSET_PATH, value))
            sprites_dict[key][index] = scale_image(image, SCALE_FACTOR)
    else:
        image = pygame.image.load(os.path.join(ASSET_PATH, value))
        sprites_dict[key] = scale_image(image, SCALE_FACTOR)