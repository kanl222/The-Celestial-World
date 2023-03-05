import pygame, sys
import config
from screen_effect import Darking, Dark_screen, ScreenEffectList, Load_screen
from threading import Thread
from support import import_folder_json
from events import *
from level import Level
from debug import debug_mode
from main_menu import MainMenu

pygame.init()
pygame.display.set_caption('The Сelestial World')


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.sittings['width'], config.sittings['height']), pygame.DOUBLEBUF)
        self.up_layer = ScreenEffectList()
        self.clock = pygame.time.Clock()
        self.menu = MainMenu(self.start_game)
        self.data = import_folder_json()
        self.frame = self.menu_
        self.flag_game = False
        self.level = None

    def terminate(self):
        pygame.quit()
        sys.exit()

    def set_size_screen(self):
        self.screen = pygame.display.set_mode((config.sittings['width'], config.sittings['height']), pygame.DOUBLEBUF)

    def set_visible_mouse(self, isVisible: bool):
        pygame.mouse.set_visible(isVisible)

    def start_game(self, data_player: dict = None):
        self.flag_game = True
        self.create_level(data_player)
        self.up_layer.add(Load_screen(time=1000, end_fun=self.frame_game), Darking())



    def create_level(self,data_player):
        self.level = Level(self.data)
        self.level.screen_effect = self.up_layer
        self.level.create_player(data_player)

    def exit_game(self):
        self.set_visible_mouse(True)
        self.level.music_channel.stop()
        self.flag_game = False
        self.frame = self.menu_

    def set_volume(self,event_dict:dict):
        pygame.mixer.music.set_volume(event_dict['volume'])
        if self.flag_game:
            self.level.music_channel.set_volume(event_dict['volume'])

    def frame_game(self):
        self.frame = self.game

    def menu_(self, events):
        self.menu.update(events)

    def game(self, events):
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
                    self.exit_game()
                elif event.type == SAVEGAME:
                    self.level.save()
                elif event.type == LOADLASTSAVE:
                    self.level.load()
                elif event.type == SETVISIBLEMOUSE:
                    self.set_visible_mouse(event.__dict__['isVisible'])
                elif event.type == SETSIZESCREEN:
                    self.set_size_screen()
                elif event.type == SETVOLUME:
                    self.set_volume(event.__dict__)
            self.screen.fill(config.WATER_COLOR)
            self.frame(events)
            self.up_layer.update()
            pygame.display.flip()
            self.clock.tick(config.FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
