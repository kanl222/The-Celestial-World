from pygame import sprite,math,time
from math import sin


class Entity(sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.12
        self.direction = math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'vertical':
            for obstacle_sprite in self.obstacle_sprites:
                if obstacle_sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = obstacle_sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = obstacle_sprite.hitbox.bottom

        if direction == 'horizontal':
            for obstacle_sprite in self.obstacle_sprites:
                if obstacle_sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = obstacle_sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = obstacle_sprite.hitbox.right


    def get_position(self) -> math.Vector2:
        return math.Vector2(self.rect.center)
