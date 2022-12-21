import pygame as pg


class EffectsList( pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self,entity):
        [sprite.update(entity) for sprite in self.sprites()]

    def __repr__(self):
        return f"{[sprite for sprite in self.sprites()]}"

    def __str__(self):
        return f"{[sprite for sprite in self.sprites()]}"



class Effect(pg.sprite.Sprite):
    def __init__(self, data):
        super(Effect, self).__init__()
        self.power = data['power']
        self.duration = data['duration']
        self.icon = data["icon"]
        self.rect = self.icon.get_rect()
        self.start_time = pg.time.get_ticks()

    def __repr__(self):
        return f'{self.__class__.__name__}{self.power, self.duration}'


class Ignition(Effect):
    """Дебаф воспламенение"""
    def __init__(self,data:dict):
        super(Ignition, self).__init__(data)

    def update(self,entity):
        print(entity)

class Weakness(Effect):
    """Дебаф слабость"""
    def __init__(self, data:dict):
        super(Weakness, self).__init__(data)

    def update(self,entity):
        print(entity)
        self.kill()

class Blind(Effect):
    def __init__(self,data:dict):
        super(Blind, self).__init__(data)

    def update(self,entity):
        print(entity)

class Regeneration(Effect):
    def __init__(self, data:dict):
        super(Regeneration, self).__init__(data)

    def update(self,entity):
        print(entity)

print(EffectsList.__name__)

