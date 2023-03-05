import pygame as pg
import json


class DialogSystem:
    def __init__(self, name: str):
        self.display_surface = pg.display.get_surface()
        self.width, self.height = self.display_surface.get_size()
        self.font = pg.font.SysFont('Comfortaa Light', 30)
        self.name = name
        self.data = self.import_data_dialogs()
        self.time = pg.time.get_ticks()

        self.id_farther = '1'
        self.text = ""
        self.text_list = []
        self.variants = {}
        self.flag = False
        self.flag_known = False

    def import_data_dialogs(self) -> dict:
        with open(f"../data/npc/{self.name}/dialogs/{self.name}.json", 'r',
                  encoding='utf-8') as file_:
            data = json.load(file_)
            return data if data else {}
            
    def render_text_shadow(self, text: str, pos: tuple, align: str) -> None:
        text_shadow = self.font.render(text, True, 'black')
        text_shadow_rect = text_shadow.get_rect(**{f'{align}': pos})
        text = self.font.render(text, True, 'white')
        text_rect = text.get_rect(**{f'{align}': pos})
        self.display_surface.blit(text_shadow, text_shadow_rect)
        self.display_surface.blit(text, text_rect)

    def render_message(self) -> None:
        if self.text:
            self.render_text_shadow(f'{self.name}: {self.text}', (self.width // 2, self.height // 8 * 7), 'center')

    def render_variants(self) -> None:
        if self.variants:
            variants_keys = list(self.variants.keys())
            variants_keys.sort(reverse=True)
            font_height = self.font.get_height()
            start_x = self.width // 4
            start_y = self.height // 2
            for i, key in enumerate(variants_keys):
                x, y = start_x, start_y + font_height * i + 10
                variant_text = f'{i + 1}) {self.variants[key][0]}'
                self.render_text_shadow(variant_text, (x, y), 'topleft')

    def update_text_list(self) -> None:
        if self.id_farther in self.data and not self.text_list and not self.variants and self.flag:
            if self.data[self.id_farther]['type'] == 'speaking':
                self.text_list = self.data[self.id_farther]['text'][:]
                self.text = self.text_list.pop(0)
            else:
                self.variants = self.data[self.id_farther]['variants']
        elif self.id_farther == 'Exit':
            self.flag = False
            self.id_farther = '1'
            if not self.flag_known:
                self.flag_known = True

    def update_text(self) -> None:
        keys = pg.key.get_pressed()
        current_time = pg.time.get_ticks()
        if not self.text_list:
            return
        if (keys[pg.K_SPACE] and current_time - self.time >= 200) or current_time - self.time >= 5000:
            self.text = self.text_list.pop(0)
            self.time = pg.time.get_ticks()
            if not self.text:
                self.id_farther = self.data[self.id_farther]['farther']

    def update_variants(self) -> None:
        keys = pg.key.get_pressed()
        if not self.variants:
            return
        variant_keys = range(49, 49 + len(self.variants))
        if any(filter(lambda x: keys[x], variant_keys)):
            variant_num = list(filter(lambda x: keys[x], variant_keys))[0] % 7 + 1
            variant_id = self.variants[str(variant_num)][1]
            self.id_farther = variant_id
            self.variants = {}

    def update(self) -> None:
        self.update_text()
        self.update_variants()
        self.update_text_list()
        self.render_message()
        self.render_variants()
