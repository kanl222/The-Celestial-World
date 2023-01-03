import pygame


class StaticObject(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['Sprite']

        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(-40, -200)
        self.hitbox.midbottom = self.rect.midbottom
