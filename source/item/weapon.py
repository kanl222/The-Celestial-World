import pygame


class Weapon():
    def __init__(self,):
        self.cooldown = 100
        self.damage =  15


class WeaponSprite(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]
        self.image = pygame.Surface((50,50))

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