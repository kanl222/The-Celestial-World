import pygame
from sitting import *
ui_font = 'serif'
pygame.font.init()

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # bar setup
        self.screen_size = self.width,self.heigth = self.display_surface.get_size()
        health_bar_width, bar_heigth = 430, 28
        self.health_bar_rect = pygame.Rect(150, 44, health_bar_width, bar_heigth)
        self.energy_bar_rect = pygame.Rect(150, 94, 360, 28)
        self.image = pygame.image.load('../graphics/interface2.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(10, 10))

    def create_text_level(self, level,rect):
        Level_text = pygame.font.SysFont(ui_font, 64).render(str(level), True,
                                                             'white')
        Level_text_rect = Level_text.get_rect(center=(180//2,rect.get_size()[1]//2 + 5))
        return self.display_surface.blit(Level_text, Level_text_rect)


    def indicator(self, current, max_amount,bg_rect):
        indicator_text = pygame.font.SysFont(ui_font, 20).render(f'{int(current)}/{int(max_amount)}', True,
                                                             'white')
        indicator_rect = indicator_text.get_rect(center=(bg_rect.center))
        return self.display_surface.blit(indicator_text,indicator_rect)


    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, '#c0c0c0', bg_rect, 3)
        return bg_rect

    def magic_overlay(self,player):
        bg_rect = self.selection_box(80, self.heigth - 120)
        magic_surf = player.magic['Icon']
        magic_surf = pygame.transform.scale(magic_surf,(ITEM_BOX_SIZE-10,ITEM_BOX_SIZE-10))
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)


    def display(self,player):
        #topleft
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect,
                      'red')
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect,
                      'blue')
        self.display_surface.blit(self.image, self.rect)
        self.indicator(player.health, player.stats['health'], self.health_bar_rect)
        self.indicator(player.energy, player.stats['energy'], self.energy_bar_rect)
        self.create_text_level(player.level,self.image)
        self.magic_overlay(player)



