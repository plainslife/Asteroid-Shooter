import pygame
from random import randint, uniform

from pygame.math import Vector2 as vector
from settings import S_WIDTH, S_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)

        # random sizes for the asteroid image
        self.image = pygame.image.load('../graphics/meteor.png') 

        # scale the original image
        scale_size = pygame.math.Vector2(self.image.get_size()) * uniform(0.5, 1.5)
        self.scaled_image = pygame.transform.scale(self.image, scale_size) # need for asteroid rotation, original image

        # make the resized image be the image of the asteroid
        self.image = self.scaled_image

        self.rect = self.image.get_frect(center = (randint(-100, S_WIDTH+100), randint(-100, -50))) # randomize start location of asteroid
        self.direction = vector(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)

        # rotation
        self.rotation = 0
        self.rotation_speed = randint(20, 50)

    def rotate(self, dt):
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.scaled_image, self.rotation, 1)

    def move(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

    def destruct(self):
        # delete the asteroid instance when it is ouside below the screen
        if self.rect.top >= S_HEIGHT: self.kill()

    def update(self, dt):
        self.move(dt)
        self.rotate(dt)
        self.destruct()

