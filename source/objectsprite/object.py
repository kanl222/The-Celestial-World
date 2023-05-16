import pygame as pg
from config import PATH_SPRITES, PATH_ANIMATIONS, TILESIZE
from support import import_folder, import_image

class Object(pg.sprite.Sprite):
    def __init__(self,data: dict, pos: tuple, groups: list):
        super().__init__(groups)
        if not data:
            self.image = pg.Surface((64,64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0,0)
            self.sprite_type = 'invisible'
        else:
            self.name = data.get('name',"test")
            self.image = self.get_sprite()
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(*data['hitbox_offset'])
            self.sprite_type = 'object'
        self.hitbox.midbottom = self.rect.midbottom


    def get_sprite(self) -> pg.Surface:
        return import_image(f"{PATH_SPRITES}/objects/{self.name}.png")

    def animation_frames(self) -> list[pg.Surface,]:
        return import_folder(f"{PATH_ANIMATIONS}/{self.name}")