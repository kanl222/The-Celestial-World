import pygame, sys
from sitting import FPS
from level import Level
from debug import debug_mode


pygame.init()

def terminate():
    pygame.quit()
    sys.exit()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280,720), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.level = Level()

        main_sound = pygame.mixer.Sound('../Music/es_barefoot-adventures.mp3')
        main_sound.set_volume(0.1)
        main_sound.play(loops=-1)
        pygame.mouse.set_visible(False)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            self.level.run()
            debug_mode(self)
            pygame.display.flip()
            self.clock.tick(FPS)
            self.screen.fill('black')

if __name__ == '__main__':
    game = Game()
    game.run()