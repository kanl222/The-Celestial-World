import pygame as pg


class StaticObject(pg.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        if not data:
            self.image = pg.Surface((64,64))
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0,0)
            self.sprite_type = 'invisible'
        else:
            self.image = data['sprite']
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(*data['hitbox_offset'])
            self.sprite_type = 'object'
        self.hitbox.center = self.rect.center
