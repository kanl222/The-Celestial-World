import pygame,sys
import config
from config import UPGRADE_BG_COLOR_SELECTED
from events import *
from widget import Menu,ListButtons,button
from time import perf_counter

# Set up Pygame
pygame.init()
win = pygame.display.set_mode((600, 600))
# Creates an array of buttons


class GameOverMenu(Menu):
    def __init__(self):
        width, height = config.sittings["width"], config.sittings['height']
        super(GameOverMenu, self).__init__((300,200),width//2,height//2)
        self.buttons_main_menu = ListButtons()
        self.background = pygame.Surface((width,height),pygame.SRCALPHA)
        self.background_rect = self.background.get_rect()
        self.background.fill('black')
        self.resume_button = self.create_button(20, 1 * 50, width=260,
                                                height=40, text='Загрузить сохранение',
                                                onClick=lambda: self.load(),
                                                group=self.buttons_main_menu)
        self.exit_button = self.create_button(20, 2 * 50 , width=260,
                                              height=40, text='Выйти',
                                              onClick=lambda: self.exit(),
                                              group=self.buttons_main_menu)
        self.font = pygame.font.SysFont('sans-serif', 80)
        self.text_pause  = self.font.render('Вы погибли',True,'red')
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

    def load(self):
        pygame.event.post(pygame.event.Event(LOADLASTSAVE))

    def exit(self):
        pygame.event.post(pygame.event.Event(EXITINMENU))

    def draw(self):
        self.surface_interface.fill('white')
        self.frame(self.surface_interface)

    def update(self,events):
        self.display_surface.blit(self.background,self.background_rect)
        self.draw()
        self.buttons_main_menu.update(events)
        self.display_surface.blit(self.surface_interface,self.rect)
        self.display_surface.blit(self.text_pause,self.text_pause_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
        self.up = GameOverMenu()
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

