import pygame, sys
from Sitting import FPS
from Level import Level
from Debug import debug_mode


pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.level = Level()

        main_sound = pygame.mixer.Sound('../Music/es_barefoot-adventures.mp3')
        main_sound.set_volume(0.1)
        main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.level.run()
            debug_mode(self)
            pygame.display.flip()
            self.clock.tick(FPS)
            self.screen.fill('black')

if __name__ == '__main__':
    game = Game()
    game.run()