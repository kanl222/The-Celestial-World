import pygame
import sys
class ScreenEffectList(pygame.sprite.Group):
    def update(self, *args, **kwargs) -> None:
        if self.sprites(): self.sprites()[0].update(*args, **kwargs)

class Darking(pygame.sprite.Sprite):
    def __init__(self,reverse=False):
        super(Darking, self).__init__()
        size = pygame.display.get_surface().get_size()
        self.surface = pygame.Surface(size,pygame.SRCALPHA)
        self.surface.fill('black')
        self.rect = self.surface.get_rect()
        self.time = pygame.time.get_ticks()
        self.speed = 2
        self.flag_reverse = reverse
        self.alpha = 255 if not reverse else 0
        self.surface.set_alpha(self.alpha)

    def update(self,screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= 500:
            self.surface.set_alpha(self.alpha)
            if 0 <= self.alpha <= 255:
                self.alpha -= self.speed if not self.flag_reverse else -self.speed
                print(self.alpha)
            else:
                self.kill()
        screen.blit(self.surface,self.rect)


class Dark_screen(pygame.sprite.Sprite):
    def __init__(self,reverse=False):
        super(Dark_screen, self).__init__()
        size = pygame.display.get_surface().get_size()
        self.surface = pygame.Surface(size,pygame.SRCALPHA)
        self.surface.fill('black')
        self.rect = self.surface.get_rect()
        self.time = pygame.time.get_ticks()


    def update(self,screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= 10**4:
            self.kill()
        screen.blit(self.surface,self.rect)
