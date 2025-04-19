import pygame
from settings import S_WIDTH, S_HEIGHT

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/laser.png')
        self.rect = self.image.get_frect(midbottom = pos)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 500

        # sound
        self.explosion_sound = pygame.mixer.Sound('../sounds/explosion.wav') # collision sound

    def collision(self, asteroid_sprites):
        if pygame.sprite.spritecollide(self, asteroid_sprites, True):
            self.explosion_sound.play()
            self.kill()

    def move(self, dt):
        self.rect.midtop += self.direction * self.speed * dt

    def destruct(self):
        # destroy the laser instance if it goes outside the screen
        if self.rect.bottom <= 0: self.kill()

    def update(self, dt, asteroid_sprites):
        self.move(dt)
        self.collision(asteroid_sprites)
        self.destruct()


class Ship(pygame.sprite.Sprite):
    def __init__(self, game, groups, laser_sprites) -> None:
        super().__init__(groups)
        self.game = game
        self.laser_sprites = laser_sprites
        self.image = pygame.image.load('../graphics/ship.png')
        self.rect = self.image.get_frect(center = pygame.mouse.get_pos())

        # shoot timer
        self.can_shoot = True
        self.shoot_time = 0

        # sound
        self.laser_sound = pygame.mixer.Sound('../sounds/laser.ogg')
        self.explosion_sound = pygame.mixer.Sound('../sounds/explosion.wav') # collision

    def collision(self, asteroid_sprites) -> None:
        # horizontal collision
        if self.rect.right >= S_WIDTH: self.rect.right = S_WIDTH
        elif self.rect.left <= 0: self.rect.left = 0

        # vertical collision
        if self.rect.bottom >= S_HEIGHT: self.rect.bottom = S_HEIGHT
        elif self.rect.top <= 0: self.rect.top = 0

        if pygame.sprite.spritecollide(self, asteroid_sprites, True):
            self.game.game_active = False
            self.explosion_sound.play()

    def move(self):
        self.rect.center = pygame.mouse.get_pos()

    # space = shooting laser
    def shoot_laser(self) -> None:

        # ship can shoot every 500 ms
        if pygame.time.get_ticks() - self.shoot_time > 500:
            self.can_shoot = True

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self.laser_sprites, pos=self.rect.midtop)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def update(self, asteroid_sprites) -> None:
        self.move()
        self.shoot_laser()
        self.collision(asteroid_sprites)

