import pygame
from config import sittings, UPGRADE_BG_COLOR_SELECTED
from events import LOADLASTSAVE, EXITINMENU
from .widget import Menu, ListButtons, button

class GameOverMenu(Menu):
    def __init__(self):
        super().__init__((300, 200), sittings['width'] // 2, sittings['height'] // 2)
        self.buttons_main_menu = ListButtons()
        self.background = pygame.Surface((sittings['width'], sittings['height']), pygame.SRCALPHA)
        self.background_rect = self.background.get_rect()
        self.background.fill('black')
        self.resume_button = self.create_button(20, 1 * 50, width=260, height=40, text='Загрузить сохранение',
                                                onClick=self.load, group=self.buttons_main_menu)
        self.exit_button = self.create_button(20, 2 * 50, width=260, height=40, text='Выйти',
                                              onClick=self.exit, group=self.buttons_main_menu)
        self.font = pygame.font.SysFont('sans-serif', 80)
        self.text_pause = self.font.render('Вы погибли', True, 'red')
        self.text_pause_rect = self.text_pause.get_rect(midbottom=(self.rect.midtop[0], self.rect.midtop[1] - 40))

    def create_button(self, x, y, width=25, height=25, text='', onClick=lambda: print(1), group=None):
        _button = button(self.surface_interface, self.rect, x, y, width, height,
                          text=text, fontSize=30, margin=10,
                          inactiveColour=UPGRADE_BG_COLOR_SELECTED, shadowColour='black',
                          pressedColour='grey', radius=1, borderThickness=2, borderColour='#c0c0c0', onClick=onClick)
        if group is not None:
            group.append(_button)
        return _button

    def load(self):
        pygame.event.post(pygame.event.Event(LOADLASTSAVE))

    def exit(self):
        pygame.event.post(pygame.event.Event(EXITINMENU))

    def draw(self):
        self.surface_interface.fill('white')
        self.frame(self.surface_interface)

    def update(self, events):
        self.display_surface.blit(self.background, self.background_rect)
        self.draw()
        self.buttons_main_menu.update(events)
        self.display_surface.blit(self.surface_interface, self.rect)
        self.display_surface.blit(self.text_pause, self.text_pause_rect)
