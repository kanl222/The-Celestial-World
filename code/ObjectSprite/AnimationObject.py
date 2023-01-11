import pygame


class DestructibleObjtect(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'animation_object'
        self.display_surface = pygame.display.get_surface()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = data['animation']
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(0, 0)
        self.hitbox.midbottom = self.rect.midbottom

    def animate(self):
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index)%len(self.frames)]

    def update(self):
        self.animate()