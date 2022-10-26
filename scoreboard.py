import pygame as pg
from pygame.sprite import Group
from ship import Ship

import random


class Scoreboard:
    def __init__(self, game):
        f = open('high_score.txt', 'r')
        data = f.read()
        self.highScore = data
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 48)
        self.alien_points1 = 10
        self.alien_points2 = 30
        self.alien_points3 = 50
        self.ufo_points = random.uniform(50, 200)

        self.score_image = None
        self.score_rect = None
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        #self.prep_ships()

    def increment_ufo_score(self):
        self.settings.score += self.ufo_points
        self.prep_score()
        self.prep_level()

    def increment_score1(self):
        self.settings.score += self.alien_points1
        self.prep_score()
        self.prep_level()
        #self.prep_ships()

    def increment_score2(self):
        self.settings.score += self.alien_points2
        self.prep_score()
        self.prep_level()

    def increment_score3(self):
        self.settings.score += self.alien_points3
        self.prep_score()
        self.prep_level()

    def prep_score(self):
        rounded_score = int(round(self.settings.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = round(self.settings.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.settings.score > self.settings.high_score:
            self.settings.high_score = self.settings.score
            self.prep_high_score()

    def prep_level(self):
        self.level_image = self.font.render(str(self.settings.level), True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    #def prep_ships(self):
        #self.ships = Group()
        #for ship_number in range(self.settings.ship_limit):
            #ship = Ship(game=self)
            #ship.image = pg.transform.scale(ship.image, (41, 70))
            #ship.rect.x = 10 + ship_number * ship.rect.width
            #ship.rect.y = 10
            #self.ships.add(ship)

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.ships.draw(self.screen)
        
