"""
Flappy bird Score class
Responsible for counting and rendering the score to the screen
"""

from assets.__init__ import sprites_dict

class Score:
    """
    Score class
    For every instance of the game, there should be a single score class instance

    image contains all of the pygame loaded sprites for digits 0-9
    """
    IMGS = sprites_dict["nums"]

    def __init__(self):
        """
        Constructor for Score class
        """
        self.score = 0
        self._rect = []
        self.IMGS = [number.convert_alpha() for number in self.IMGS]
                     

    @property             
    def score(self):
        return self._score
    
    @property
    def score_to_string(self):
        return str(self.score)
    
    @score.setter
    def score(self, val):
        self._score = val
    
    @property
    def get_img(self):
        """
        Detects the amount of digits in the score, then constructs a list containing the number sprites needed

        :return: type: list
            List of pygame sprites with the numbers that make up the score
        """
        if (digits := len(self.score_to_string)) > 1:
            return [self.IMGS[int(self.score_to_string[number])] for number in range(0, digits)]

        return [self.IMGS[self._score]]
    
    def draw(self, win):
        """
        Loops the all digits of the score and draw/renders the player's score into the game screen digit by digit

        :param screen: type: pygame.surface
        The surface/screen of the game for displaying purposes
        """
        img_list = self.get_img
        img_width_list = [img.get_width() for img in img_list]
        self._rect = []

        for index, number in enumerate(img_list, start = 0):
            self._rect.append(win.blit(number,
                                    (sprites_dict['bg-day'].get_width() / 2 - sum(img_width_list) * 1 + sum(img_width_list[0:index]),
                                     sprites_dict['bg-day'].get_height() / 8)
            ))
