import pygame, sys
from Sitting import FPS
from level import Level
from debug import debug_mode



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.level = Level()

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
            pygame.display.update()
            self.clock.tick(FPS)
            self.screen.fill('black')



if __name__ == '__main__':
    game = Game()
    game.run()