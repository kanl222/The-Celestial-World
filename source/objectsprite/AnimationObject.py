import pygame as pg
from .object import Object

class AnimationObject(Object):
    def __init__(self,data: dict, pos: tuple, groups: list):
        super().__init__(data, pos, groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = self.animation_frames()
        self.image = self.frames[int(self.frame_index)]

    def animate(self):
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index)%len(self.frames)]

    def update(self):
        self.animate()