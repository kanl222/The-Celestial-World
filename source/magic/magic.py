import pygame
from enum import Enum
from config import PATH_ICONS, PATH_ANIMATIONS, TILESIZE
from support import import_folder, import_image,import_animation
from effects import Effect, get_effect


class MagicType(Enum):
    BULLET = 1
    ON_ENEMY = 2
    ON_PLAYER = 3
    LINE = 4
    AREA = 5


class Magic:
    def __init__(self, data: dict, magic_logic):
        self.sprite_type = 'magic'
        self.name: str = data['name']
        self.name.split()
        self.magic_type: MagicType = MagicType[data['type'].rsplit('_', 1)[0].upper()]
        self.cost: int = data['cost']
        self.damage: int = data['damage']
        self.cooldown: int = data['cooldown'] * 1000
        self.range: int = data['range']
        self.upgrade_level: int = data['upgrade_level']
        self.element: str = data['element']
        self.icon = self.icon_image()

        if self.magic_type == MagicType.BULLET:
            self.flight_range: int = data['flight_range'] * TILESIZE
            self.animation = magic_logic.bullet_magic
        elif self.magic_type == MagicType.ON_ENEMY:
            self.radius: int = data['radius'] * TILESIZE
            self.animation = magic_logic.on_enemy_magic
        elif self.magic_type == MagicType.ON_PLAYER:
            self.animation = magic_logic.on_player
        elif self.magic_type == MagicType.LINE:
            self.duration: int = data['duration'] * TILESIZE
            self.animation = magic_logic.line_magic
        elif self.magic_type == MagicType.AREA:
            self.radius: int = data['radius'] * TILESIZE
            self.animation = magic_logic.area_magic

        self.effect: Effect = self.create_effect(data)

    def create_effect(self, data: dict) -> Effect:
        if 'effect' in data:
            effect_data = data['effect']
            name = effect_data['name']
            return get_effect(name)(effect_data)
        else:
            return None


    def icon_image(self) -> pygame.Surface:
        return import_image(f"{PATH_ICONS}/magics/{self.name}.png")

    def animation_frames(self) -> list[pygame.Surface]:
        try:
            return import_folder(f"{PATH_ANIMATIONS}/{self.name}",key_sorted=lambda e: int(e.rsplit('_', 1)[1].rsplit('.', 1)[0]))
        except Exception as e:
            print(e)

    def create_magic(self, player: object, groups: list) -> None:
        try:
            self.animation(player, self, groups)
        except Exception as e:
            print(e)
