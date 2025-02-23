from assets.__init__ import sprites_dict


class Score:
    IMGS = sprites_dict["nums"]

    def __init__(self):
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
        if (digits := len(self.score_to_string)) > 1:
            return [self.IMGS[int(self.score_to_string[number])] for number in range(0, digits)]

        return [self.IMGS[self._score]]
    
    def draw(self, win):
        img_list = self.get_img
        img_width_list = [img.get_width() for img in img_list]
        self._rect = []

        for index, number in enumerate(img_list, start = 0):
            self._rect.append(win.blit(number,
                                    (sprites_dict['bg-day'].get_width() / 2 - sum(img_width_list) * 1 + sum(img_width_list[0:index]),
                                     sprites_dict['bg-day'].get_height() / 8)
            ))
