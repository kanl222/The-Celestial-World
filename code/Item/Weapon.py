import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.queue = 1
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]
        self.image = pygame.Surface((50,50)).convert_alpha()

        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(
                midleft=player.rect.center)
        elif direction == 'left':
            self.rect = self.image.get_rect(
                midright=player.rect.center )
        elif direction == 'down':
            self.rect = self.image.get_rect(
                midtop=player.rect.center )
        else:
            self.rect = self.image.get_rect(
                midbottom=player.rect.center)