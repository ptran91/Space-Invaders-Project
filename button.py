import pygame as pg


class Button:
    def __init__(self, settings, screen, msg):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 150, 40
        self.button_color = (0, 0, 0)
        self.text_color = (118, 238, 0)
        self.font = pg.font.SysFont(None, 36)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (602, 600)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Space:
    def __init__(self, settings, screen, msg):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 150, 40
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 90)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (602, 70)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Invaders:
    def __init__(self, settings, screen, msg):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 150, 40
        self.button_color = (0, 0, 0)
        self.text_color = (118, 238, 0)
        self.font = pg.font.SysFont(None, 90)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (602, 130)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Points:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pg.image.load("images/points.png")
        self.rect = self.image.get_rect()
        self.rect.center = (602, 350)
        self.prep_msg()

    def prep_msg(self):
        self.msg_image_rect = self.image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.blit(self.image, self.msg_image_rect)


class Highscores:
    def __init__(self, settings, screen, msg):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 150, 40
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 36)
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = (602, 650)
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)