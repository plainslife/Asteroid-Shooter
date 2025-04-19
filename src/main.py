import pygame, sys, time

from settings import S_WIDTH, S_HEIGHT, FPS
from text import Text
from background import Background
from player import Ship
from asteroid import Asteroid

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Asteroid Shooter")
        self.screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.high_score = 0
        self.score = 0

        # font 
        self.font = pygame.font.Font('../fonts/subatomic.ttf', 50)

        # music 
        bg_music = pygame.mixer.Sound('../sounds/music.wav')
        bg_music.play(loops=-1)

        # groups
        self.laser_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()
        self.ship_sprite = pygame.sprite.GroupSingle()

        # game background
        self.background = Background()

        # ship i.e player
        self.ship = Ship(self, self.ship_sprite, self.laser_sprites)

        # custom events
        self.spawn_asteroid = pygame.event.custom_type()
        pygame.time.set_timer(self.spawn_asteroid, 500)

    def start_menu(self):
        if self.score > self.high_score: self.high_score = self.score

        Text((S_WIDTH//2, 300), "Asteroid Shooter", 50, 'white').draw(self.screen)
        Text((74, 65), f"Score: {self.score}", 25, 'white').draw(self.screen)
        Text((110, 35), f"High Score: {self.high_score}", 25, 'white').draw(self.screen)
        Text((S_WIDTH//2, 500), "Press Space To Start", 50, 'white').draw(self.screen)

        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.current_time = pygame.time.get_ticks()
            self.score = 0
            self.asteroid_sprites.empty()
            self.laser_sprites.empty()
            self.game_active = True

    def display_score(self):
        self.score = (pygame.time.get_ticks() - self.current_time) // 1000
        score_text = Text((S_WIDTH//2, 700), f'{self.score}', 50, 'white')
        score_text.draw(self.screen)

    def run(self):
        prev_time = time.time()
        while True:

            # delta-time
            dt = time.time() - prev_time
            prev_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == self.spawn_asteroid and self.game_active:
                    Asteroid([self.asteroid_sprites])

            self.background.draw(self.screen)

            if self.game_active:
                # update
                self.ship_sprite.update(self.asteroid_sprites)
                self.laser_sprites.update(dt, self.asteroid_sprites)
                self.asteroid_sprites.update(dt)

                # draw to screen
                self.display_score() 
                self.ship_sprite.draw(self.screen)
                self.laser_sprites.draw(self.screen)
                self.asteroid_sprites.draw(self.screen)
                
            else:
                self.start_menu()

            # limit fps
            self.clock.tick(FPS)

            # update things on the screen
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
