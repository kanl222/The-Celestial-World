import pygame as pg
from .object import Object

class DestructibleObjtect(Object):
    def __init__(self,data: dict, pos: tuple, groups: list):
        super().__init__(data, pos, groups)
        pass
