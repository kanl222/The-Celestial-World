import pygame, sys
from config import FPS,WATER_COLOR,WIDTH,HEIGTH
from support import import_folder_json
from events import SETVISIBLEMOUSE,RESUME,EXITINMENU,SAVEGAME
from level import Level
from debug import debug_mode
from main_menu import MainMenu


pygame.init()



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH), pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self.start_game)
        self.data = import_folder_json()
        self.frame = self.menu_

    def terminate(self):
        pygame.quit()
        sys.exit()

    def set_visible_mouse(self,isVisible:bool):
        pygame.mouse.set_visible(isVisible)

    def start_game(self, player_info = None):
        self.level = Level(self.data,player_info)
        self.frame = self.game

    def menu_(self,events):
        self.menu.update(events)

    def game(self,events):
        self.level.run(events)
        debug_mode(self)

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == RESUME:
                    self.level.resume()
                elif event.type == EXITINMENU:
                    self.frame = self.menu_
                elif event.type == SAVEGAME:
                    self.level.save()
                elif event.type == SETVISIBLEMOUSE:
                    self.set_visible_mouse(event.__dict__['isVisible'])


            self.frame(events)
            pygame.display.flip()
            self.clock.tick(FPS)
            self.screen.fill(WATER_COLOR)

if __name__ == '__main__':
    game = Game()
    game.run()