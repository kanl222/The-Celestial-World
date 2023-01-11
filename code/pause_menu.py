import pygame,sys
from config import *
from events import *
from widget import Menu,ListButtons,button
from time import perf_counter
Width,height= 1280,720
# Set up Pygame
pygame.init()
win = pygame.display.set_mode((600, 600))
# Creates an array of buttons


class PauseMenu(Menu):
    def __init__(self):
        super(PauseMenu, self).__init__((300,300),WIDTH//2,HEIGTH//2)
        self.buttons_main_menu = ListButtons()
        self.background = pygame.Surface((WIDTH,HEIGTH),pygame.SRCALPHA)
        self.background_rect = self.background.get_rect()
        self.background.fill('black')
        self.background.set_alpha(180)
        self.resume_button = self.create_button(20, 1 * 50, width=260,
                                                height=40, text='Продолжить',
                                                onClick=lambda: self.resume(),
                                                group=self.buttons_main_menu)
        self.sittings_button = self.create_button(20, 3 * 50 , width=260,
                                                  height=40, text='Настройки',
                                                  onClick=lambda: self.sittings(),
                                                  group=self.buttons_main_menu)
        self.saves_button = self.create_button(20, 2 * 50, width=260,
                                                  height=40, text='Сохранить',
                                                  onClick=lambda: self.save(),
                                                  group=self.buttons_main_menu)
        self.exit_button = self.create_button(20, 4 * 50 , width=260,
                                              height=40, text='Выйти',
                                              onClick=lambda: self.exit(),
                                              group=self.buttons_main_menu)
        self.font = pygame.font.SysFont('sans-serif', 80)
        self.text_pause  = self.font.render('Пауза',True,'white')
        x,y = self.rect.midtop
        self.text_pause_rect = self.text_pause.get_rect(midbottom=(x,y-40))



    def create_button(self, x=0, y=0, width=25, height=25, text='',onClick=lambda: print(1), group=None):
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

    def resume(self):
        pygame.event.post(pygame.event.Event(RESUME))

    def save(self):
        pygame.event.post(pygame.event.Event(SAVEGAME))

    def sittings(self):
        pygame.event.post(pygame.event.Event(SETVISIBLEMOUSE))

    def exit(self):
        pygame.event.post(pygame.event.Event(EXITINMENU))

    def draw(self):
        self.surface_interface.fill('white')
        self.frame()

    def update(self,events):
        self.display_surface.blit(self.background,self.background_rect)
        self.draw()
        self.buttons_main_menu.update(events)
        self.display_surface.blit(self.surface_interface,self.rect)
        self.display_surface.blit(self.text_pause,self.text_pause_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
        self.up = PauseMenu()
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


            self.up.update(events)
            pygame.display.update()
            self.clock.tick(60)
            self.screen.fill('white')
if __name__ == '__main__':
    print(pygame.USEREVENT)
    game = Game()
    game.run()

