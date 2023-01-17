import pygame


class DestructibleObjtect(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['sprite']
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-40, -170)
        self.hitbox.midbottom = self.rect.midbottom
