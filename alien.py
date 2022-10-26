from random import randint
import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer
from pygame import mixer
from random import randrange
speed = 0


class Alien(Sprite):
    green_alien_images = [pg.image.load(f'images/green_alien{n}.png') for n in range(2)]
    blue_alien_images = [pg.image.load(f'images/blue_alien{n}.png') for n in range(2)]
    red_alien_images = [pg.image.load(f'images/red_alien{n}.png') for n in range(2)]

    alien_timers = {2: Timer(image_list=green_alien_images), 1: Timer(image_list=blue_alien_images),
                    0: Timer(image_list=red_alien_images)}

    alien_explosion_images = [pg.image.load(f'images/explosion{n}.png') for n in range(8)]

    #alien_scores = {2: 10, 1: 20, 0: 30}

    def __init__(self, game, type):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        #self.score = Alien.alien_scores[type]

        self.green = pg.image.load('images/green_alien0.png')
        self.rect = self.green.get_rect()
        self.green_value = 10

        self.blue = pg.image.load('images/blue_alien0.png')
        self.rect = self.blue.get_rect()
        self.blue_value = 20

        self.red = pg.image.load('images/red_alien0.png')
        self.rect = self.red.get_rect()
        self.red_value = 30

        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.sb = game.scoreboard
        self.sound = game.sound

        self.dying = self.dead = False

        self.timer_normal = Alien.alien_timers[type]
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, is_loop=False)
        self.timer = self.timer_normal

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
            self.sb.increment_score1()
            self.sb.check_high_score()
            self.sb.prep_level()

    def update(self):
        global speed
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
            speed += 1
            if speed % 10 == 0:
                self.game.ominous_music()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.fleet_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)


class Aliens:
    def __init__(self, game):
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()

        self.ship_lasers = game.ship_lasers.lasers
        self.aliens_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.barrier = game.barriers
        self.create_fleet()
        self.alien_sound = mixer.Sound('sounds/enemy_explosion.wav')
        self.ship_sound = mixer.Sound('sounds/ship_explosion.wav')

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (1 * alien_height))
        number_rows = 6
        return number_rows

    def reset(self):
        global speed
        self.aliens.empty()
        self.create_fleet()
        self.aliens_lasers.reset()
        speed = 0

    def create_alien(self, alien_number, row_number):
        type = row_number // 2
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.4 * alien_width * alien_number
        alien.rect.x = alien.x * 2
        alien.rect.y = alien.rect.height + 1 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width)
        number_rows = self.get_number_rows(self.ship.rect.height, self.model_alien.rect.height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()
                self.alien_sound.play()
                self.alien_sound.set_volume(0.5)

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()
            self.ship_sound.play()
            self.ship_sound.set_volume(0.5)

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        for alien in self.aliens.sprites():
            if alien.dead:
                alien.remove()
            alien.update()
        self.aliens_lasers.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()


class Ufo(Sprite):
    ufo_images = [pg.image.load(f'images/ufo{n}.png') for n in range(2)]

    alien_timers = {1: Timer(image_list=ufo_images)}

    alien_explosion_images = [pg.image.load(f'images/explosion{n}.png') for n in range(8)]

    def __init__(self, game, type):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        self.ufo_image = pg.image.load('images/ufo0.png')
        self.rect = self.ufo_image.get_rect()

        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.sb = game.scoreboard

        self.dying = self.dead = False

        self.timer_normal = Ufo.alien_timers[type]
        self.timer_explosion = Timer(image_list=Ufo.alien_explosion_images, is_loop=False)
        self.timer = self.timer_normal

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
            self.sb.increment_ufo_score()
            self.sb.check_high_score()
            self.sb.prep_level()

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += (settings.alien_speed_factor * settings.ufo_direction)
        self.rect.x = self.x
        self.draw()

    def draw(self):
        ufo_image = self.timer.image()
        rect = ufo_image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(ufo_image, rect)


class Ufos:
    def __init__(self, game):
        self.model_ufo = Ufo(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.ufos = Group()

        self.ship_lasers = game.ship_lasers.lasers
        self.aliens_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0
        self.ship = game.ship
        self.barrier = game.barriers
        self.create_ufo()
        self.ufo_image = pg.image.load('images/ufo0.png')
        self.rect = self.ufo_image.get_rect()
        self.rect.x = randrange(self.settings.screen_width - self.rect.width)
        self.rect.bottom = randrange(-80, -20)

    def reset(self):
        self.ufos.empty()
        self.create_ufo()
        self.aliens_lasers.reset()

    def create_ufo(self):
        type = 1
        ufo = Ufo(game=self.game, type=type)
        alien_width = ufo.rect.width
        ufo.x = alien_width + 2 * alien_width
        ufo.rect.y = 0
        self.ufos.add(ufo)

    def check_ufo_edges(self):
        for ufo in self.ufos.sprites():
            self.rect.x += self.settings.ufo_speed_factor_x * self.settings.ufo_direction
            self.rect.y += self.settings.ufo_speed_factor_y
            if ufo.check_edges():
                self.rect.y += self.settings.ufo_drop_speed
                self.settings.ufo_direction *= -1
                break

    def check_ufo_bottom(self):
        for ufo in self.ufos.sprites():
            if ufo.check_bottom_or_ship(self.ship):
                self.ship.hit()
                break

    def check_ufo_empty(self):
        if len(self.ufos.sprites()) == 0:
            self.game.reset()

    def change_ufo_direction(self):
        for ufo in self.ufos.sprites():
            ufo.rect.y += self.settings.ufo_drop_speed
        self.settings.ufo_direction *= -1

    def shoot_from_random_ufo(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.ufos.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.ufos.sprites():
            if i == alien_num:
                self.aliens_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.ufos, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()

        collisions = pg.sprite.spritecollide(self.ship, self.aliens_lasers.lasers, True)
        if collisions:
            self.ship.hit()

    def update(self):
        self.check_ufo_edges()
        self.check_ufo_bottom()
        self.check_collisions()
        self.check_ufo_empty()
        self.shoot_from_random_ufo()
        for ufo in self.ufos.sprites():
            if ufo.dead:
                ufo.remove()
            ufo.update()
        self.aliens_lasers.update()

    def draw(self):
        for ufo in self.ufos.sprites():
            ufo.draw()

