import pygame as pg

class DialogSystem:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.height = self.display_surface.get_height() // 8 * 7
        self.width = self.display_surface.get_width() // 2
        self.font = pg.font.SysFont('Comfortaa Light', 30)
        self.message_ = ''
        self.speak_ = ''

    def message(self,mes):
        self.message_ = mes
        Level_text_shadow = self.font.render(mes, True, 'black')
        Level_text_rect_shadow = Level_text_shadow.get_rect(center=(self.width+1, self.height+1))
        Level_text = self.font.render(mes, True,'white')
        Level_text_rect = Level_text.get_rect(center=(self.width,self.height))
        self.display_surface.blit(Level_text_shadow, Level_text_rect_shadow)
        return self.display_surface.blit(Level_text, Level_text_rect)

    def speaking(self,mes):
        self.speak_ = mes
        Level_text_shadow = self.font.render(mes, True, 'black')
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            center=(self.width //2 + 1, self.height //2 + 1))
        Level_text = self.font.render(mes, True, 'white')
        Level_text_rect = Level_text.get_rect(center=(self.width //2, self.height //2))
        self.display_surface.blit(Level_text_shadow, Level_text_rect_shadow)
        return self.display_surface.blit(Level_text, Level_text_rect)

    def update(self):
        self.message(self.message_)
        self.speaking(self.speak_)


