import pygame, sys
import config
from config import UI_BG_COLOR,translation
import pygame_widgets
from widget import button,ListButtons,Menu




class Upgrade(Menu):
    def __init__(self,player):
        width, height = config.sittings["width"], config.sittings['height']
        super(Upgrade, self).__init__((500, 600),width // 4*3, height // 2)
        self.player = player
        self.buttons = ListButtons()
        self.character = self.player.character
        self.character_keys = list(self.character.keys())
        self.top_ = 20
        self.ColorTextShadow = 'black'
        self.ColorText = '#f3f3f3'

        for i in range(len(self.character_keys)):
            self.create_button(400,self.top_ + (i + 1) * 45, text='+',
                               onClick=lambda i=i: self.Upgrade_stats(self.character_keys[i]))
    def update_date(self):
        self.stats = self.player.stats
        self.stats_keys = list(self.stats.keys())

    def Upgrade_stats(self, stat):
        self.character[stat] += 1
        self.player.point_character -= 1
        self.player.update_stats()


    def create_button(self, x=0, y=0, width=25, height=25, text='',
                      onClick=lambda: print(1)):
        self.buttons.append(button(
            self.surface_interface, self.rect, x, y, width, height, text=text,
            fontSize=30, margin=10,
            inactiveColour='white',
            pressedColour='grey',textColour='red', radius=1,
            borderThickness=2,
            borderColour='#c0c0c0',
            onClick=onClick
        ))


    def draw(self):
        self.update_date()
        self.surface_interface.fill(UI_BG_COLOR)
        self.create_topleft_text(60,30,f'Очки характеристик: {self.player.point_character} ')
        y_ = 30
        for i in range(len(self.character_keys)):
            y = self.top_ + (i + 1) * 45 + 2
            self.create_topleft_text(60,y, text=f'{translation[self.character_keys[i]]}:')
            self.create_topleft_text(300,y, text=f'{self.character[self.character_keys[i]]}')
            y_ = y
        y_ += 35
        pygame.draw.line(self.surface_interface, '#c0c0c0',(30, y_),( self.rect.w - 30, y_), 2)
        y_ += 25
        self.create_center_text(self.rect.w//2, y_, f'Характеристика')
        y_ +=25
        pygame.draw.line(self.surface_interface, '#c0c0c0', (30, y_),
                         (self.rect.w - 30, y_), 2)
        for i in range(len(self.stats_keys)):
            y = 360 + (i + 1) * 35 + 2
            self.create_topleft_text(60,y, text=f'{translation[self.stats_keys[i]]}:')
            self.create_topleft_text(300,y, text=f'{self.stats[self.stats_keys[i]]}')
        self.frame(self.surface_interface)


    def update(self,events):
        if self.player.point_character:self.buttons.enable()
        else: self.buttons.disable()
        self.draw()
        self.buttons.update(events)
        self.display_surface.blit(self.surface_interface, self.rect)

class Player:
    def __init__(self):
        self.point_character = 5
        self.stats = {'health': 5, 'energy': 5,
                      'attack': 5, 'magic': 5, 'speed': 5}
        self.character = {'health': 5, 'energy': 5, 'power': 5, 'intelligence': 5,
                          'body_type': 5, 'dexterity': 5}



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
        self.player = Player()
        self.up = Upgrade(self.player)
        self.clock = pygame.time.Clock()
        self.n = {'les': 1}

    def terminate(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.terminate()
            self.up.update(self.screen)
            pygame.display.update()
            self.clock.tick(60)
            self.screen.fill('black')


if __name__ == '__main__':
    pygame.init()
    win = pygame.display.set_mode((600, 600))
    game = Game()
    game.run()
