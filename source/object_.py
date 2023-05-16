import pygame
from objectsprite import *

class ObjectGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def add_static_object(self, data: dict, pos: tuple, groups: list):
        static_obj = StaticObject(data, pos, groups)
        self.add(static_obj)

    def add_destructible_object(self, data: dict, pos: tuple, groups: list):
        destructible_obj = DestructibleObjtect(data, pos, groups)
        self.add(destructible_obj)

    def add_moving_object(self, data: dict, pos: tuple, groups: list, destination: tuple):
        moving_obj = MovingObject(data, pos, groups, destination)
        self.add(moving_obj)

    def add_animated_object(self, data: dict, pos: tuple, groups: list, animation_frames: list):
        animated_obj = AnimationObject(data, pos, groups, animation_frames)
        self.add(animated_obj)

    def add_trigger_object(self, data: dict, pos: tuple, groups: list, trigger_function: callable):
        trigger_obj = TriggerObject(data, pos, groups, trigger_function)
        self.add(trigger_obj)
