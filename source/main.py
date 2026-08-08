import json
import os

import pygame
import sys
from pathlib import Path
from screen_effect import Darking, DarkScreen, ScreenEffectList, LoadScreen
from concurrent.futures import ThreadPoolExecutor
import config
from support import import_folder_json, BASE_DIR
from events import *
from game_logic import GameLogic
from debug import debug_mode
from interfaces.main_menu import MainMenu

# Путь к config.json, независимый от рабочей директории
_CONFIG_PATH: Path = BASE_DIR / 'assets' / 'config.json'

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
        self.screen_effect.add(LoadScreen(pool=self.future), Darking())
        self.is_init_game = False
        self.frame = self._menu
        self.flag_game = False
        # Строим таблицу обработчиков один раз — не пересоздаём каждый кадр
        self._event_handlers: dict = self._build_event_handlers()


        
    @staticmethod
    def save_settings() -> None:
        """Cохраняет настройки в файл."""
        with _CONFIG_PATH.open('w', encoding='utf-8') as f:
            json.dump(config.settings, f)

    @staticmethod
    def load_settings() -> None:
        """Zагружает настройки из файла."""
        with _CONFIG_PATH.open('r', encoding='utf-8') as f:
            config.settings = json.load(f)
            config.sittings = config.settings  # поддерживаем синхронизацию алиасов

    def load_or_create_settings(self) -> None:
        """Zагружает настройки если файл есть, иначе создаёт с значениями по умолчанию."""
        if _CONFIG_PATH.exists():
            self.load_settings()
        else:
            _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with _CONFIG_PATH.open('w', encoding='utf-8') as f:
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

    def _build_event_handlers(self) -> dict:
        """Строит таблицу обработчиков событий. Вызывается один раз при инициализации."""
        return {
            pygame.QUIT:      lambda e: self.terminate(),
            SETVOLUME:        lambda e: self.game.music.change_volume(e.__dict__['volume']),
            TOGGLEFULLSCREEN: lambda e: self.toggle_fullscreen(),
            SAVESETTINGS:     lambda e: self.save_settings(),
            LOADSETTINGS:     lambda e: self.load_settings(),
            RESUME:           lambda e: self.game.resume(),
            EXITINMENU:       lambda e: self.exit_in_menu(),
            SAVEGAME:         lambda e: self.game.save(),
            LOADLASTSAVE:     lambda e: self.game.load(),
            SETVISIBLEMOUSE:  lambda e: self.set_visible_mouse(e.__dict__['isVisible']),
            SETSIZESCREEN:    lambda e: self.set_size_screen(),
        }

    def run(self) -> None:
        """Основной игровой цикл."""
        while True:
            # 1. Получаем события ОДИН РАЗ за кадр
            events = pygame.event.get()

            # 2. Обрабатываем события через таблицу
            for event in events:
                if event.type in self._event_handlers:
                    self._event_handlers[event.type](event)

            # 3. Очищаем экран ПЕРЕД отрисовкой (правильный порядок: fill → draw → flip)
            self.screen.fill(config.WATER_COLOR)

            # 4. Обновляем и отрисовываем текущий экран
            self.frame(events)
            self.screen_effect.update(events)

            # 5. Проверяем готовность фонового потока инициализации
            if not self.is_init_game and self.future.done():
                self.game = self.future.result()
                self.is_init_game = True

            # 6. Показываем готовый кадр и ограничиваем FPS
            pygame.display.flip()
            self.clock.tick(config.FPS)



if __name__ == '__main__':
    game = Game()
    game.run()
