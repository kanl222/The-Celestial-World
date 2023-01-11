import pygame
from config import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # bar setup
        self.screen_size = self.width,self.heigth = self.display_surface.get_size()
        health_bar_width, bar_heigth = 430, 28
        self.health_bar_rect = pygame.Rect(150, 44, health_bar_width, bar_heigth)
        self.energy_bar_rect = pygame.Rect(150, 94, 360, 28)
        self.image = pygame.image.load('../graphics/interface.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(10, 10))
        self.font = pygame.font.SysFont('sans-serif', 30)
        self.ColorTextShadow='black'
        self.ColorText='#F8F9FB'

    def create_center_text(self,screen, x=0, y=0,font=pygame.font.Font(None,30), text=''):
        Level_text_shadow = font.render(text, True, self.ColorTextShadow)
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            center=(x + 1, y + 1))
        Level_text = font.render(text, True, self.ColorText)
        Level_text_rect = Level_text.get_rect(center=(x, y))
        screen.blit(Level_text_shadow, Level_text_rect_shadow)
        screen.blit(Level_text, Level_text_rect)

    def create_text_level(self, level):
        font = pygame.font.Font(None, 78)
        text = font.render(str(level), True,COLOR_FONT)
        text_rect = text.get_rect(center=(90,self.rect.h//2+10))
        self.display_surface.blit(text, text_rect)


    def indicator(self, current, max_amount,bg_rect):
        font = pygame.font.Font(UI_FONT, 18)
        indicator_text = font.render(f'{int(current)}/{int(max_amount)}', True,COLOR_FONT)
        indicator_rect = indicator_text.get_rect(center=(bg_rect.center))
        self.display_surface.blit(indicator_text,indicator_rect)


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
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        x,y=bg_rect.topleft
        pygame.draw.rect(self.display_surface, '#8c8c8c',(x+1, y+1, bg_rect.w - 2, bg_rect.h - 2), 1)
        pygame.draw.rect(self.display_surface, '#404040',(x+3, y+3, bg_rect.w - 3, bg_rect.h - 3), 1)
        return bg_rect

    def magic_overlay(self,player):
        bg_rect = self.selection_box(60, self.heigth - 120)
        magic_surf = player.magic['icon']
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
        self.create_text_level(player.level)
        self.magic_overlay(player)



