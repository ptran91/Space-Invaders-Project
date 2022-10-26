from settings import Settings
import game_functions as gf
from laser import Lasers, LaserType
from alien import *
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers
from button import *
import sys


class Game:
    speed = 0

    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek0.wav")
        self.scoreboard = Scoreboard(game=self)

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)

        self.play_button = Button(self.settings, self.screen, "PLAY GAME")
        self.space_title = Space(self.settings, self.screen, "SPACE")
        self.invaders_title = Invaders(self.settings, self.screen, "INVADERS")
        self.hs_button = Highscores(self.settings, self.screen, f'HIGH SCORE: {self.scoreboard.highScore}')
        self.points = Points(self.settings, self.screen)

        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.ufos = Ufos(game=self)
        self.settings.initialize_speed_settings()

    def reset(self):
        self.barriers.reset()
        self.ship.reset()
        self.ufos.reset()
        self.ominous_music()

    def game_over(self):
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def ominous_music(self):
        self.speed += 1
        pg.mixer.music.load(f'sounds/startrek{self.speed}.wav')
        pg.mixer.music.set_volume(0.7)
        pg.mixer.music.play(-1, 0.0)

    def play(self):
        self.sound.play_bg()
        while True:

            if not self.settings.game_active:
                self.play_button.draw_button()
                self.points.draw_button()
                self.hs_button.draw_button()
                self.space_title.draw_button()
                self.invaders_title.draw_button()

            gf.check_events(settings=self.settings, ship=self.ship, play_button=self.play_button)
            if self.settings.game_active:
                background = pg.image.load(f'images/background.jpg').convert()
                self.screen.blit(background, (0, 0))
                self.ship.update()
                self.aliens.update()
                self.ufos.update()
                self.scoreboard.update()
                self.barriers.update()
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
