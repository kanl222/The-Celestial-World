import pygame


class StaticObject(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['Sprite']
        if data['Name'].split('_')[0] == 'Tree':
            self.image = pygame.transform.scale(self.image,
                                                (self.image.get_size()[0] * 3,
                                                 self.image.get_size()[1] * 3))
        print(self.image.get_size())
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(-40, -200)
        self.hitbox.midbottom = self.rect.midbottom
