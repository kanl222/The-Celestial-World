import pygame as pg
from .object import Object


class MovingObject(Object):
    def __init__(self,data: dict, pos: tuple, groups: list):
        super().__init__(data, pos, groups)
        self.velocity = [0, 0]

    def update(self, dt):
        dx = self.velocity[0] * dt # по оси x
        dy = self.velocity[1] * dt # по оси y
        self.rect.move_ip(dx, dy)
        self.hitbox.move_ip(dx, dy)
