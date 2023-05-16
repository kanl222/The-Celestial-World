import json
import os

import pygame
import sys
from screen_effect import Darking, DarkScreen, ScreenEffectList, LoadScreen
from concurrent.futures import ThreadPoolExecutor
import config
from support import import_folder_json
from events import *
from game_logic import GameLogic
from debug import debug_mode
from interfaces.main_menu import MainMenu

pygame.init()
pygame.display.set_caption('The Celestial World')


def initialize_game(data,screen_effect):
    game = GameLogic(data, screen_effect)
    return game

class Game:
    def __init__(self):
        self.load_or_create_settings()
        size = (config.settings['width'], config.settings['height'])
        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.data = import_folder_json()
        self.screen_effect = ScreenEffectList()
        self.menu = MainMenu(self.start_game)
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.future = self.thread_pool.submit(initialize_game, self.data, self.screen_effect)
        self.screen_effect.add(LoadScreen(pool=self.future),Darking())
        self.is_init_game = False
        self.frame = self._menu
        self.flag_game = False


        
    @staticmethod
    def save_settings():
        with open('../assets/config.json', 'w') as f:
            json.dump(config.settings, f)

    @staticmethod
    def load_settings():
        with open('../assets/config.json', 'r') as f:
            config.settings = json.load(f)

    def load_or_create_settings(self):
        if os.path.exists('../assets/config.json'):
            self.load_settings()
        else:
            with open('../assets/config.json', 'w') as f:
                json.dump(config.settings, f)

    def terminate(self):
        pygame.quit()
        sys.exit()
        
    def set_size_screen(self):
        size = (config.settings['width'], config.settings['height'])
        self.screen = pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF, vsync=1)

    def set_visible_mouse(self, set_visible: bool):
        pygame.mouse.set_visible(set_visible)

    def start_game(self, player_info=None):
        self.flag_game = True
        self.game.init_player(player_info)
        self.frame = self._game

    def _menu(self, events):
        self.menu.update(events)

    def _game(self, events):
        self.game.run(events)
        debug_mode(self)

    def toggle_fullscreen(self):
        config.settings['fullscreen'] = not config.settings['fullscreen']
        if config.settings['fullscreen']:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.set_size_screen()

    def exit_in_menu(self):
        self.set_visible_mouse(True)
        self.game.music.stop_music()
        self.flag_game = False 
        self.game.reset_game_logic()
        self.frame = self._menu

    def run(self):
        while True:
            event_handlers = {
            pygame.QUIT: lambda e: self.terminate(),
            SETVOLUME: lambda e: self.game.music.change_volume(e.__dict__['volume']),
            TOGGLEFULLSCREEN: lambda e: self.toggle_fullscreen(),
            SAVESETTINGS: lambda e: self.save_settings(),
            LOADSETTINGS: lambda e: self.load_settings(),
            RESUME: lambda e: self.game.resume(),
            EXITINMENU: lambda e: self.exit_in_menu(),
            SAVEGAME: lambda e: self.game.save(),
            LOADLASTSAVE: lambda e: self.game.load(),
            SETVISIBLEMOUSE: lambda e: self.set_visible_mouse(e.__dict__['isVisible']),
            SETSIZESCREEN: lambda e: self.set_size_screen(),
            }
            events = pygame.event.get()

            while True:
                events = pygame.event.get()

                for event in events:
                    if event.type in event_handlers:
                        event_handlers[event.type](event)  
                self.frame(events)
                self.screen_effect.update(events)      
                if not self.is_init_game and self.future.done():
                    self.game = self.future.result()
                    self.is_init_game = True
                pygame.display.flip()
                self.clock.tick(config.FPS)
                self.screen.fill(config.WATER_COLOR)



if __name__ == '__main__':
    game = Game()
    game.run()
