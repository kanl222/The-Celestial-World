import pygame as pg
from support import import_image
from config import PATH_ICONS
from elemets import Damage

class EffectsList(pg.sprite.Group):
    def __init__(self,entity):
        super().__init__()
        self.entity = entity

    def __str__(self):
        return f"{[sprite for sprite in self.sprites()]}"
        
    def add_effect(self, effect):
        self.add(effect)

    def remove_effect(self, effect):
        self.remove(effect)
        
    def update_effects(self):
        for effect in self.sprites():
            effect.update(self.entity)


    def __mul__(self, other):
        return other * (sum(self) + 1)

    __imul__ = __mul__
    __rmul__ = __mul__
    __repr__ = __str__




class Effect(pg.sprite.Sprite):
    """Bазовый класс временного эффекта на энтитет."""
    def __init__(self, data):
        super().__init__()
        self.power = data['power']
        self.duration = data['duration'] * 1000
        self.cooldown = 2000  # исправлена опечатка: cooldawn → cooldown
        self.time_last = pg.time.get_ticks()
        self.start_time = pg.time.get_ticks()

    def __repr__(self):
        return f'{self.__class__.__name__}{self.power, self.duration}'

    def __int__(self):
        return self.power / 100

    def __radd__(self, other):
        return self.power / 100 + other

    def update_duration(self):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.kill()

    def update_start_time(self):
        self.start_time = pg.time.get_ticks()

    def update(self, entity) -> None:
        """Oбновляет длительность эффекта и применяет его с учётом cooldown."""
        self.update_duration()
        current_time = pg.time.get_ticks()
        if current_time - self.time_last >= self.cooldown:
            self.apply_effect(entity)
            self.time_last = pg.time.get_ticks()

    def import_image(self, path: str) -> pg.Surface:
        """Zагружает изображение иконки эффекта."""
        return pg.image.load(path).convert_alpha()

class Strength(Effect):
    def __init__(self, data):
        #self.icon = self.import_image(f"{PATH_ICONS}/effect/{self.__class__.__name__}.png")
        super().__init__(data)


    def apply_effect(self, entity):
        entity.strength += self.power

class Burning(Effect):
    def __init__(self, data):
        #self.icon = self.import_image(f"{PATH_ICONS}/effect/{self.__class__.__name__}.png")
        super().__init__(data)
        self.damage = Damage(self.power,self.__class__.__name__)

    def apply_effect(self, entity):
        entity.get_damage_effect(self.damage)

class Poison(Effect):
    """Eффект отравления: периодически наносит урон."""
    def __init__(self, data):
        super().__init__(data)
        self.damage = Damage(self.power, self.__class__.__name__)

    def apply_effect(self, entity):
        entity.get_damage_effect(self.damage)

class HealthBoost(Effect):
    def __init__(self, data):
        #self.icon = self.import_image(f"{PATH_ICONS}/effect/{self.__class__.__name__}.png")
        super().__init__(data)

    def apply_effect(self, entity):
        entity.health += self.power

class Weakness(Effect):
    def __init__(self, data):
        #self.icon = self.import_image(f"{PATH_ICONS}/effect/{self.__class__.__name__}.png")
        super().__init__(data)

    def apply_effect(self, entity):
        entity.strength -= self.power

class Blind(Effect):
    def __init__(self, data):
        #self.icon = self.import_image(f"{PATH_ICONS}/effect/{self.__class__.__name__}.png")
        super().__init__(data)

    def apply_effect(self, entity):
        pass

class Regeneration(Effect):
    def __init__(self, data):
        #self.icon = self.import_image(f"{PATH_ICONS}/effect/{self.__class__.__name__}.png")
        super().__init__(data)

    def apply_effect(self, entity):
        entity.health += self.power




# Реестр эффектов: добавление нового эффекта не требует изменения get_effect()
_EFFECT_REGISTRY: dict[str, type[Effect]] = {
    cls.__name__.lower(): cls
    for cls in [Burning, Poison, HealthBoost, Strength, Weakness, Blind, Regeneration]
}


def get_effect(effect_name: str) -> type[Effect] | None:
    """Vозвращает класс эффекта по имени или None, если эффект не найден.

    Пример:
        get_effect('burning') -> Burning
        get_effect('unknown') -> None
    """
    return _EFFECT_REGISTRY.get(effect_name.lower())
