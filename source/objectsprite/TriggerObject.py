import pygame
from .object import Object

class TriggerObject(Object):
    def __init__(self, data: dict, pos: tuple, groups: list, trigger_function: callable):
        super().__init__(data, pos, groups)
        self.velocity = [0, 0]
        self.trigger_function = trigger_function

    def update(self, dt: int):
        dx = self.velocity[0] * dt # по оси x
        dy = self.velocity[1] * dt # по оси y
        self.rect.move_ip(dx, dy)
        self.hitbox.move_ip(dx, dy)

    def on_collide(self, other_sprite: pygame.sprite.Sprite) -> None:
        if other_sprite.rect.colliderect(self.hitbox):
            self.trigger_function()


