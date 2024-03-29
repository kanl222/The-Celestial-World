import pygame, sys
import config
from config import UPGRADE_BG_COLOR_SELECTED
from save_game_system import check_saves
from .widget import button, ListButtons, _TextBox, Menu
from .sittings import SittingsMenu


class MainMenu(Menu):
    def __init__(self, start_game):
        width, height = config.sittings["width"], config.sittings['height']
        super(MainMenu, self).__init__((340, 360), width // 12 * 10.2, height // 2)
        self.background = pygame.image.load(
            f'../graphics/backgrounds/main_menu/background_{width}x{height}.png')
        self.background_rect = self.background.get_rect()
        self.sittings = SittingsMenu()
        pygame.mixer.music.load('../music/Ambient 1.mp3')
        pygame.mixer.music.set_volume(config.sittings["volume_music"])
        pygame.mixer.music.play()
        self.start_game = start_game
        self.ColorTextShadow = 'grey'
        self.ColorText = 'black'
        padding_top = 20
        self.buttons_main_menu = ListButtons()
        self.resume_button = self.create_button(20, 2 * 50 - padding_top, width=300,
                                                height=40, text='Продолжить',
                                                onClick=lambda: self.resume(),
                                                group=self.buttons_main_menu)
        self.new_game_button = self.create_button(20, 3 * 50 - padding_top, width=300,
                                                  height=40, text='Новая игра',
                                                  onClick=lambda: self.new_game(),
                                                  group=self.buttons_main_menu)
        self.sittings_button = self.create_button(20, 4 * 50 - padding_top, width=300,
                                                  height=40, text='Настройки',
                                                  onClick=lambda: self._sittings_menu(),
                                                  group=self.buttons_main_menu)
        self.exit_button = self.create_button(20, 5 * 50 - padding_top, width=300,
                                              height=40, text='Выйти',
                                              onClick=lambda: self.exit(),
                                              group=self.buttons_main_menu)
        self.buttons_new_game_menu = ListButtons()

        self.start_button = self.create_button(20, 5 * 50, width=300,
                                               height=40, text='Начать',
                                               onClick=lambda: self.start(),
                                               group=self.buttons_new_game_menu)
        self.back_button = self.create_button(20, 6 * 50, width=300,
                                              height=40, text='Назад',
                                              onClick=lambda: self.back(),
                                              group=self.buttons_new_game_menu)
        self.human_button = self.create_button(20, 3 * 50, width=140,
                                               height=40, text='Человек',
                                               onClick=lambda: self.choice_human(),
                                               group=self.buttons_new_game_menu)
        self.elf_button = self.create_button(180, 3 * 50, width=140,
                                             height=40, text='Эльф',
                                             onClick=lambda: self.choice_elf(),
                                             group=self.buttons_new_game_menu)
        self.textbox = _TextBox(self.surface_interface, self.rect, 20, 48, 300, 30,
                                fontSize=30,
                                borderColour='#c0c0c0', borderThickness=2,
                                colour='#EEEEEE',
                                textColour='black',
                                onSubmit=self.submit)
        self.buttons_new_game_menu.append(self.textbox)
        self.buttons_new_game_menu.hide()

        self.buttons = self.buttons_main_menu
        self.menu = self.main_menu

    def exit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def submit(self):
        self.player_data["name"] = self.textbox.getText()

    def resume(self):
        pygame.mixer.music.fadeout(2000)
        self.main_menu()
        self.start_game()

    def _sittings_menu(self):
        self.menu = self.sittings_menu
        self.buttons_main_menu.hide()
        self.buttons = None

    def set_volume(self,volume):
        pygame.mixer.music.set_volume(volume)

    def choice_elf(self):
        self.player_data["species"] = "elf"

    def choice_human(self):
        self.player_data["species"] = "human"

    def start(self):
        pygame.mixer.music.fadeout(2000)
        self.start_game(self.player_data)
        self.back()

    def new_game(self):
        self.menu = self.new_game_menu
        self.buttons = self.buttons_new_game_menu
        self.buttons_main_menu.hide()
        self.buttons_new_game_menu.show()

        self.player_data = {"name": "", "species": "human"}

    def sittings_menu(self, events):
        if not self.sittings.flag_exit:
            self.sittings.update(events)
        else:
            self.sittings.flag_exit = not self.sittings.flag_exit
            self.buttons = self.buttons_main_menu
            self.menu = self.main_menu
            self.buttons_main_menu.show()

    def back(self):
        self.buttons = self.buttons_main_menu
        self.menu = self.main_menu
        self.buttons_new_game_menu.hide()
        self.buttons_main_menu.show()

    def create_button(self, x=0, y=0, width=25, height=25, text='',
                      onClick=lambda: print(1), group=None):
        _button = button(
            self.surface_interface, self.rect, x, y, width, height, text=text,
            fontSize=30, margin=10,
            inactiveColour=UPGRADE_BG_COLOR_SELECTED, shadowColour='black',
            pressedColour='grey', radius=1,
            borderThickness=2,
            borderColour='#c0c0c0',
            onClick=onClick)
        if group is not None:
            group.append(_button)
        return _button

    def main_menu(self):
        if check_saves():
            self.resume_button.enable()
        else:
            self.resume_button.disable()

        if not pygame.mixer.music.get_busy(): pygame.mixer.music.play()

    def new_game_menu(self):
        self.create_topleft_text(20, 20, 'Имя персонажа:')
        self.create_topleft_text(20, 120, 'Выбор расы:')

    def draw(self):
        self.surface_interface.fill('#f3f3f3')
        self.frame(self.surface_interface)

    def update(self, events):
        self.display_surface.blit(self.background, self.background_rect)
        if self.buttons is None: return self.menu(events)
        self.draw()
        self.menu()
        self.buttons.update(events)
        self.display_surface.blit(self.surface_interface, self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
        self.up = MainMenu(self.start_game)
        self.clock = pygame.time.Clock()

        self.flag_menu = True

    def start_game(self, player_info: dict):
        self.flag_menu = False

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.terminate()
            self.up.update(events)
            pygame.display.update()
            self.clock.tick(60)
            self.screen.fill('black')


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
