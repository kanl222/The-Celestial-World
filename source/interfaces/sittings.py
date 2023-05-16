import pygame, sys
import config
from config import UPGRADE_BG_COLOR_SELECTED
from events import *
from support import save_config
from .widget import Menu, ListButtons, button, _Slider
from time import perf_counter


class SittingsMenu(Menu):
    def __init__(self):
        width, height = config.sittings["width"], config.sittings['height']
        super(SittingsMenu, self).__init__((600, 600), width // 2,
                                           height // 2)
        self.buttons_sittings_menu = ListButtons()
        self.surface_frame = pygame.Surface((570, 480))
        self.rect_frame = self.surface_frame.get_rect(topleft=(15, 70))
        self.management_button = self.create_button(self.surface_interface, self.rect, 15,
                                                    20, width=180,
                                                    height=40, text='Управление',
                                                    onClick=lambda: self.management(),
                                                    group=self.buttons_sittings_menu)
        self.screen_button = self.create_button(self.surface_interface, self.rect, 210,
                                                20, width=180,
                                                height=40, text='Экран',
                                                onClick=lambda: self.screen(),
                                                group=self.buttons_sittings_menu)
        self.audio_button = self.create_button(self.surface_interface, self.rect, 405, 20,
                                               width=180,
                                               height=40, text='Аудио',
                                               onClick=lambda: self.audio(),
                                               group=self.buttons_sittings_menu)
        self.accept_button = self.create_button(self.surface_interface, self.rect, 405,
                                                552,
                                                width=180,
                                                height=40, text='Принять',
                                                onClick=lambda: self.accept(),
                                                group=self.buttons_sittings_menu, )
        self.back_button = self.create_button(self.surface_interface, self.rect, 220,
                                              552,
                                              width=180,
                                              height=40, text='Назад',
                                              onClick=lambda: self.back(),
                                              group=self.buttons_sittings_menu, )
        self.sitting_copy = config.sittings.copy()
        self.screen_sittings_menu = ListButtons()
        self.audio_sittings_menu = ListButtons()
        self.management_sittings_menu = ListButtons()
        x, y = self.rect.topleft
        x += self.rect_frame.topleft[0]
        y += self.rect_frame.topleft[1]
        self.w1920_h1080 = self.create_button(self.surface_frame, self.rect_frame, 10,
                                              50,
                                              width=180,
                                              height=40, text='1920x1080',
                                              onClick=lambda: self.set_size(1920, 1080),
                                              group=self.screen_sittings_menu, left=x,
                                              top=y)
        self.w1280_h720 = self.create_button(self.surface_frame, self.rect_frame, 10,
                                             100,
                                             width=180,
                                             height=40, text='1280x720',
                                             onClick=lambda: self.set_size(1280, 720),
                                             group=self.screen_sittings_menu, left=x,
                                             top=y)

        self.slider_VOLUME_MUSIC = _Slider(self.surface_frame, x, y, 20, 50, 530, 15,
                                           min=0, max=99,
                                           step=1, group=self.audio_sittings_menu,
                                           initial=self.sitting_copy[
                                                       'volume_music'] * 100)
        self.slider_VOLUME_MENU_EFFECT = _Slider(self.surface_frame, x, y, 20, 130, 530,
                                                 15, min=0, max=99,
                                                 step=1, group=self.audio_sittings_menu,
                                                 initial=self.sitting_copy[
                                                             'volume_effects'] * 100)
        self.sittings_translation = {"Вправо": 'button_move_right',
                                     "Вниз": 'button_move_down',
                                     "Влево": 'button_move_left',
                                     "Вверх": 'button_move_up',
                                     "Использовать магию": 'button_using_magic',
                                     "Использовать оружие": 'button_using_weapon',
                                     "Поменять магию": 'button_change_magic',
                                     "Открыть прокачку": 'button_open_menu_upgrade',
                                     }

        self.sittings_keys = list(self.sittings_translation.keys())

        for i in range(len(self.sittings_keys)):
            self.saves_button = self.create_button(self.surface_frame, self.rect_frame,
                                                   20, 50 * i + 20, width=160,
                                                   height=40, text=self.sittings_keys[i],
                                                   onClick=lambda
                                                       i=i: self.change_key_batton(
                                                       self.sittings_keys[i]),
                                                   group=self.management_sittings_menu,
                                                   fontSize=20, left=x, top=y)

        self.variable_parameter = None
        self.flag_variable_parameter_key = False
        self.ListGroups = ListButtons()
        self.ListGroups.addWidgets(
            [*self.management_sittings_menu, *self.buttons_sittings_menu])

        self.menu = self.management_menu
        self.flag_exit = False

    def change_key_batton(self, key):
        self.variable_parameter = self.sittings_translation[key]
        self.flag_variable_parameter_key = True

    def create_button(self, screen, rect, x=0, y=0, width=25, height=25,
                      color=UPGRADE_BG_COLOR_SELECTED, text='',
                      onClick=lambda: print(1), group=None, fontSize: int = 30, left=0,
                      top=0):
        _button = button(
            screen, rect, x, y, width, height, text=text,
            fontSize=fontSize, margin=10,
            inactiveColour=color, shadowColour='black',
            pressedColour='grey', radius=1,
            borderThickness=2,
            borderColour='#c0c0c0',
            onClick=onClick)
        if left and top:
            _button.left, _button.top = left, top
        if group is not None:
            group.append(_button)
        return _button

    def create_topleft_text(self, screen, x=0, y=0, text=''):
        Level_text_shadow = self.font.render(text, True, self.ColorTextShadow)
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            topleft=(x + 1, y + 1))
        Level_text = self.font.render(text, True, self.ColorText)
        Level_text_rect = Level_text.get_rect(topleft=(x, y))
        screen.blit(Level_text_shadow, Level_text_rect_shadow)
        screen.blit(Level_text, Level_text_rect)

    def back(self):
        self.sitting_copy = config.sittings.copy()
        self.flag_exit = True
        self.ListGroups = ListButtons()
        self.ListGroups.addWidgets(
            [*self.management_sittings_menu, *self.buttons_sittings_menu])

        self.menu = self.management_menu

    def accept(self):
        # if self.sitting_copy["width"] != config.sittings[ "width"] and  self.sitting_copy["height"] !=config.sittings["height"]:
        #    pygame.event.post(pygame.event.Event(SETSIZESCREEN))
        if self.sitting_copy["volume_music"] != config.sittings["volume_music"] or \
                self.sitting_copy[
                    "volume_effects"] != config.sittings["volume_effects"]:
            pygame.event.post(pygame.event.Event(SETVOLUME, volume=self.sitting_copy["volume_music"]))
        config.sittings = self.sitting_copy.copy()
        save_config(self.sitting_copy)
        self.flag_exit = True

    def management(self):
        self.menu = self.management_menu
        self.ListGroups.clear()
        self.ListGroups.addWidgets(
            [*self.management_sittings_menu, *self.buttons_sittings_menu])

    def screen(self):
        self.menu = self.screen_menu
        self.ListGroups.clear()
        self.ListGroups.addWidgets(
            [*self.screen_sittings_menu, *self.buttons_sittings_menu])

    def audio(self):
        self.menu = self.audio_menu
        self.ListGroups.clear()
        self.ListGroups.addWidgets(
            [*self.audio_sittings_menu, *self.buttons_sittings_menu])

    def set_size(self, width, heigth):
        self.sitting_copy["width"] = width
        self.sitting_copy["height"] = heigth

    def audio_menu(self, events):
        self.sitting_copy['volume_music'] = self.slider_VOLUME_MUSIC.getValue() / 100
        self.sitting_copy[
            'volume_effects'] = self.slider_VOLUME_MENU_EFFECT.getValue() / 100
        self.create_topleft_text(self.surface_frame, 20, 20,
                                 text=f'Громкость музыки: {self.slider_VOLUME_MUSIC.getValue()}')
        self.create_topleft_text(self.surface_frame, 20, 100,
                                 text=f'Громкость эффектов: {self.slider_VOLUME_MENU_EFFECT.getValue()}')

    def screen_menu(self, events):
        self.create_topleft_text(self.surface_frame, 240, 50,
                                 text=f'Текущие разрешение {config.sittings["width"]}x{config.sittings["height"]}')
        self.create_topleft_text(self.surface_frame, 240, 100,
                                 text='Новое разрешение {0}x{1}'.format(
                                     self.sitting_copy["width"] if self.sitting_copy[
                                                                       "width"] !=
                                                                   config.sittings[
                                                                       "width"] else '-----',
                                     self.sitting_copy["height"] if self.sitting_copy[
                                                                        "height"] !=
                                                                    config.sittings[
                                                                        "height"] else '-----'))

    def management_menu(self, events):
        self.ColorTextShadow = 'grey'
        self.ColorText = 'black'
        for i in range(len(self.sittings_keys)):
            self.create_topleft_text(self.surface_frame, 240, i * 50 + 30,
                                     text=f'{pygame.key.name(self.sitting_copy[self.sittings_translation[self.sittings_keys[i]]])}')
        if self.flag_variable_parameter_key:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.sitting_copy[self.variable_parameter] = event.key

    def draw(self):
        self.surface_interface.fill('white')
        self.surface_frame.fill(UPGRADE_BG_COLOR_SELECTED)
        self.frame(self.surface_interface)
        self.frame(self.surface_frame)

    def update(self, events):
        if config.sittings == self.sitting_copy:
            self.accept_button.disable()
        else:
            self.accept_button.enable()
        self.draw()
        self.menu(events)
        self.ListGroups.update(events)
        self.surface_interface.blit(self.surface_frame, self.rect_frame)
        self.display_surface.blit(self.surface_interface, self.rect)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
        self.up = SittingsMenu()
        self.clock = pygame.time.Clock()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == SAVEGAME:
                    print(23)

            self.up.update(events)
            pygame.display.update()
            self.clock.tick(60)
            self.screen.fill('white')


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
