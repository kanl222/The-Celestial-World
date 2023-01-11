import pygame as pg
import json

class DialogSystem:
    def __init__(self,name):
        self.display_surface = pg.display.get_surface()
        self.width,self.height = self.display_surface.get_size()
        self.font = pg.font.SysFont('Comfortaa Light', 30)
        self.name = name
        self.data = self.import_data_dialogs()
        self.time = pg.time.get_ticks()

        self.id_farther = '1'
        self.text =""
        self.text_list = []
        self.variants = {}
        self.flag = False
        self.flag_known = False

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
        if self.text: self.render_center_text_shadow(f'{self.name}: {self.text}',(self.width//2,self.height//8*7))

    def render_variants(self):
        if self.variants:
            list_ = list(self.variants.keys())
            list_.sort(reverse=True)
            for i in range(len(list_)):
                self.render_topleft_text_shadow(f'{i+1}) {self.variants[list_[i]][0]}', (self.width // 4, self.height // 2 + self.font.get_height()*i))

    def update_text_list(self):
        if self.id_farther in self.data.keys() and not self.text_list and not self.variants and self.flag:
            if self.data[self.id_farther]['type'] == 'speaking':
                self.text_list = self.data[self.id_farther]['text'].copy()
                self.text = self.text_list.pop(0)
            else:
                self.variants = self.data[self.id_farther]['variants']
        elif self.id_farther == 'Exit':
            self.flag = False
            self.id_farther = '1'
            if not self.flag_known:
                self.flag_known = not self.flag_known

    def update_text(self):
        keys = pg.key.get_pressed()
        current_time = pg.time.get_ticks()
        if not self.text_list: return
        if (keys[pg.K_SPACE] and current_time - self.time >= 200) or current_time - self.time >= 5000:
            self.text = self.text_list.pop(0)
            self.time = pg.time.get_ticks()
            if not self.text:
                self.id_farther = self.data[self.id_farther]['farther']

    def update_variants(self):
        keys = pg.key.get_pressed()
        if not self.variants: return
        if any(filter(lambda x: keys[x],range(49,49+ len(self.variants)))):
            self.id_farther = self.variants[str(list(filter(lambda x: keys[x],range(49,49+len(self.variants))))[0]%7+1)][1]
            self.variants = {}


    def update(self):
        self.update_text()
        self.update_variants()
        self.update_text_list()
        self.render_message()
        self.render_variants()





