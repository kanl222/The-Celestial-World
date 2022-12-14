import pygame as pg

class DialogSystem:
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.height = self.display_surface.get_height()
        self.width = self.display_surface.get_width()
        self.font = pg.font.SysFont('Comfortaa Light', 30)
        self.message_ = ''
        self.speak_ = {}

    def render_text_shadow(self,mes,pos):
        Level_text_shadow = self.font.render(mes, True, 'black')
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            topleft=(pos[0] + 1, pos[1] + 1))
        Level_text = self.font.render(mes, True, 'white')
        Level_text_rect = Level_text.get_rect(topleft=(pos[0], pos[1]))
        self.display_surface.blit(Level_text_shadow, Level_text_rect_shadow)
        self.display_surface.blit(Level_text, Level_text_rect)
        return None

    def message(self,mes):
        self.message_ = mes
        self.render_text_shadow(mes,(self.width//2,self.height//8*7))

    def speaking(self,variants:dict):
        self.speak_ = variants
        list_ = list(variants.keys())
        list_.sort(reverse=True)
        for i in range(len(list_)):
            self.render_text_shadow(f'{list_[i]}) {variants[list_[i]]}', (self.width // 4, self.height // 2 - 30*i))


    def update(self):
        self.message(self.message_)
        self.speaking(self.speak_)


