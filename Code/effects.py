import pygame as pg

class EffectsList(list):
    def __init__(self,entity):
        super().__init__()
        self.entity = entity

    def update(self):
        [i.update(self.entity) for i in self]


class Effect:
    def __init__(self, power_effect, duration_effect):
        self.power = power_effect
        self.duration = duration_effect
        self.start_time = pg.time.get_ticks()

    def __repr__(self):
        return f'{self.__class__.__name__}{self.power, self.duration}'


class Ignition(Effect):
    def __init__(self,power_effect,duration_effect):
        super(Ignition, self).__init__(power_effect,duration_effect)

    def update(self,entity):
        print(entity)

class Weaken(Effect):
    def __init__(self, power_effect, duration_effect):
        super(Weaken, self).__init__(power_effect, duration_effect)

    def update(self,entity):
        print(entity)

class Blind(Effect):
    def __init__(self, power_effect, duration_effect):
        super(Blind, self).__init__(power_effect, duration_effect)

    def update(self,entity):
        print(entity)

class Regeneration(Effect):
    def __init__(self, power_effect, duration_effect):
        super(Regeneration, self).__init__(power_effect, duration_effect)

    def update(self,entity):
        print(entity)

effect = EffectsList(1)
effect.append(Weaken(1,1))
effect.append(Weaken(1,1))
effect.append(Weaken(1,1))
print(effect)


