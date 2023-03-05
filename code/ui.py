import pygame
from config import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.image = pygame.image.load('../graphics/interface.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(10, 10))
        
        self.health_bar_rect = pygame.Rect(150, 44, 430, 28)
        self.energy_bar_rect = pygame.Rect(150, 94, 360, 28)

        self.font = pygame.font.SysFont('sans-serif', 40)

        self.indicator_font = pygame.font.Font(UI_FONT, 18)
        self.centered_font = pygame.font.Font(None, 30)

    def create_center_text(self, x, y, text):
        text_shadow = self.centered_font.render(text, True, '#000000')
        text_shadow_rect = text_shadow.get_rect(center=(x + 1, y + 1))
        text = self.centered_font.render(text, True, '#F8F9FB')
        text_rect = text.get_rect(center=(x, y))
        self.display_surface.blit(text_shadow, text_shadow_rect)
        self.display_surface.blit(text, text_rect)

    def indicator(self, current, max_amount, bg_rect):
        indicator_text = self.indicator_font.render('{}/{}'.format(int(current), int(max_amount)), True, COLOR_FONT)
        indicator_rect = indicator_text.get_rect(center=bg_rect.center)
        self.display_surface.blit(indicator_text,indicator_rect)

    def show_bar(self, current, max_amount, bg_rect, color):
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
        bg_rect = self.selection_box(60, self.display_surface.get_height() - 120)
        magic_surf = player.magic['icon']
        magic_surf = pygame.transform.scale(magic_surf,(ITEM_BOX_SIZE-10,ITEM_BOX_SIZE-10))
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self,player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, 'red')
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, 'blue')
        self.display_surface.blit(self.image, self.rect)
        self.indicator(player.health, player.stats['health'], self.health_bar_rect)
        self.indicator(player.energy, player.stats['energy'], self.energy_bar_rect)
        self.level_text = self.font.render(f'{player.level}', True, COLOR_FONT)
        self.level_text_rect = self.level_text.get_rect(center=(90,self.rect.h//2+10))
        self.display_surface.blit(self.level_text, self.level_text_rect)
        self.magic_overlay(player)



