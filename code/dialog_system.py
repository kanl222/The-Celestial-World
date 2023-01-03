import pygame as pg
import json

class DialogSystem:
    def __init__(self,name):
        self.display_surface = pg.display.get_surface()
        self.height,self.width = self.display_surface.get_size()
        self.font = pg.font.SysFont('Comfortaa Light', 30)
        self.name = name
        self.data = self.import_data_dialogs()
        self.messege = ''
        self.messeges = []
        self.variants = {}

    def import_data_dialogs(self):
            with open(f"../data/dialogs/{self.name}.json", 'r',encoding='utf-8') as file_:
                file = file_.read()
                if not file: return {}
                return json.loads(file)

    def render_center_text_shadow(self,text,pos):
        Level_text_shadow = self.font.render(text, True, 'black')
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            center=(pos[0] + 1, pos[1] + 1))
        Level_text = self.font.render(text, True, 'white')
        Level_text_rect = Level_text.get_rect(center=(pos[0], pos[1]))
        self.display_surface.blit(Level_text_shadow, Level_text_rect_shadow)
        self.display_surface.blit(Level_text, Level_text_rect)

    def render_topleft_text_shadow(self,text,pos):
        Level_text_shadow = self.font.render(text, True, 'black')
        Level_text_rect_shadow = Level_text_shadow.get_rect(
            topleft=(pos[0] + 1, pos[1] + 1))
        Level_text = self.font.render(text, True, 'white')
        Level_text_rect = Level_text.get_rect(topleft=(pos[0], pos[1]))
        self.display_surface.blit(Level_text_shadow, Level_text_rect_shadow)
        self.display_surface.blit(Level_text, Level_text_rect)

    def render_message(self):
        if self.messege:
            self.render_center_text_shadow(self.messege,(self.width//2,self.height//8*7))

    def render_variants(self):
        if self.variants:
            list_ = list(self.variants.keys())
            list_.sort(reverse=True)
            for i in range(len(list_)):
                self.render_topleft_text_shadow(f'{list_[i]}) {self.variants[list_[i]]}', (self.width // 4, self.height // 2 - self.font.get_height()*i))


    def update(self):
        keys = pg.key.get_pressed()

        self.render_message()




