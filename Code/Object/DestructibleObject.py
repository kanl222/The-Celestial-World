import pygame


class DestructibleObjtect(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['Image']
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_size()[0] * 2 + 32,
                                             self.image.get_size()[1] * 3))
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(-40, -170)
        self.hitbox.midbottom = self.rect.midbottom
