import pygame, sys
from Sitting import FPS
from level import Level
from debug import debug


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN,pygame.OPENGL)
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
            debug(self.clock.get_fps(),200,10)
            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(FPS)
            self.screen.fill('black')



if __name__ == '__main__':
    game = Game()
    game.run()