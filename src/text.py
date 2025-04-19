import pygame

# create text surfaces 
class Text:
    def __init__(self, pos, text, size, color, AA=True):
        self.font = pygame.font.Font('../fonts/subatomic.ttf', size)
        self.text = self.font.render(text, AA, color)
        self.rect = self.text.get_frect(midbottom = pos)

    def draw(self, screen):
        screen.blit(self.text, self.rect)


