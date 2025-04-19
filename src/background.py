import pygame

class Background:
    def __init__(self) -> None:
        self.image = pygame.image.load('../graphics/background.png').convert()
        self.rect = self.image.get_rect(topleft = (0,0))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


