from random import randrange


class Settings:

    def __init__(self):
        self.laser_speed_factor = None
        self.ship_speed_factor = None
        self.alien_speed_factor = None
        self.speedup_scale = None
        self.game_active = False

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        self.laser_width = 5
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 10  # change to 1 to see faster lasers

        self.aliens_shoot_every = 120  # about every 2 seconds at 60 fps

        self.ship_limit = 3  # total ships allowed in game before game over

        self.ufo_drop_speed = 1
        self.fleet_drop_speed = 1
        self.fleet_direction = 1  # change to a Vector(1, 0) move to the right, and ...
        self.ufo_direction = 10

        self.initialize_speed_settings()

        with open("high_score.txt", "r") as file_object:
            high_score = file_object.read()
            if high_score == "":
                high_score = 0

        self.high_score = int(high_score)

        self.score = 0
        self.level = 1

    def initialize_speed_settings(self):
        self.ufo_speed_factor_x = 1.0
        self.ufo_speed_factor_y = randrange(-8, -6)
        self.alien_speed_factor = 1
        self.ship_speed_factor = 15
        self.laser_speed_factor = 10

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale
