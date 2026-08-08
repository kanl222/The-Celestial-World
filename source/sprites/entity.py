import pygame
from pygame import sprite, math, time
from math import sin


class Entity(sprite.Sprite):
    """Bазовый класс для всех игровых сущностей (игрок, враг, NPC).
    Отвечает за движение, обработку коллизий и анимацию.
    """
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.12
        self.direction = math.Vector2()

    def move(self, speed: float) -> None:
        """Dвижет энтитет с учётом коллизий по двум осям."""
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction: str) -> None:
        """Oбрабатывает коллизии с препятствиями по одной оси.

        Использует spritecollide вместо ручного цикла для лучшей производительности.
        """
        hits = pygame.sprite.spritecollide(
            self, self.obstacle_sprites, False,
            collided=lambda a, b: a.hitbox.colliderect(b.hitbox)
        )
        for obstacle in hits:
            if direction == 'horizontal':
                if self.direction.x > 0:   # движение вправо
                    self.hitbox.right = obstacle.hitbox.left
                elif self.direction.x < 0: # движение влево
                    self.hitbox.left = obstacle.hitbox.right
            else:  # vertical
                if self.direction.y > 0:   # движение вниз
                    self.hitbox.bottom = obstacle.hitbox.top
                elif self.direction.y < 0: # движение вверх
                    self.hitbox.top = obstacle.hitbox.bottom

    def get_position(self) -> math.Vector2:
        """Vозвращает текущую позицию энтитета как вектор."""
        return math.Vector2(self.rect.center)
