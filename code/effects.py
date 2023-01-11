import pygame as pg


class EffectsList(pg.sprite.Group):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"{[sprite for sprite in self.sprites()]}"

    def __mul__(self, other):
        return other * (sum(self) + 1)

    __imul__ = __mul__
    __rmul__ = __mul__
    __repr__ = __str__

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

    def __int__(self):
        return self.power / 100

    def __radd__(self, other):
        return self.power / 100 + other

    def update_duration(self):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.duration: self.kill()

class Strength(Effect):
    def __init__(self, data:dict):
        super(Strength, self).__init__(data)

    def update(self,entity):
        self.duration()

class Poison(Effect):
    def __init__(self, data:dict):
        super(Poison, self).__init__(data)

    def update(self,entity):
        self.duration()

class HealthBoost(Effect):
    def __init__(self, data:dict):
        super(HealthBoost, self).__init__(data)

    def update(self,entity):
        self.duration()

class Weakness(Effect):
    def __init__(self, data:dict):
        super(Weakness, self).__init__(data)

    def update(self,entity):
        self.duration()

class Blind(Effect):
    def __init__(self,data:dict):
        super(Blind, self).__init__(data)

    def update(self,entity):
        self.duration()

class Regeneration(Effect):
    def __init__(self, data:dict):
        super(Regeneration, self).__init__(data)

    def update(self,entity):
        self.duration()


if __name__ == '__main__':

    effect_ = Effect(data={'power':10,'duration':1000,'icon':10})
    effect_1 = Effect(data={'power':20,'duration':1000,'icon':10})
    effect_2 = Effect(data={'power':20,'duration':1000,'icon':10})
    effect_3 = Effect(data={'power':20,'duration':1000,'icon':10})
    list__ = EffectsList()
    list__.add(effect_,effect_1,effect_2,effect_3)

    print(300*list__)
