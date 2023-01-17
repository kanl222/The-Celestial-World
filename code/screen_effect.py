import pygame
class ScreenEffectList(pygame.sprite.Group):
    def __init__(self):
        super(ScreenEffectList, self).__init__()
        self.screen = pygame.display.get_surface()

    def update(self) -> None:
        if self.sprites(): self.sprites()[0].update(self.screen)


class Darking(pygame.sprite.Sprite):
    def __init__(self,speed=4,sleep=500,reverse=False):
        super(Darking, self).__init__()
        self.height,self.width = size = pygame.display.get_window_size()
        self.surface = pygame.Surface(size,pygame.SRCALPHA)
        self.surface.fill('black')
        self.rect = self.surface.get_rect()
        self.time = pygame.time.get_ticks()
        self.sleep = sleep
        self.speed = speed
        self.flag_reverse = reverse
        self.alpha = 255 if not reverse else 0
        self.surface.set_alpha(self.alpha)

    def update(self,screen):
        current_time = pygame.time.get_ticks()
        if current_time - self.time >= self.sleep:
            self.surface.set_alpha(self.alpha)
            if 0 <= self.alpha <= 255:
                self.alpha -= self.speed if not self.flag_reverse else -self.speed
            else:
                self.kill()
        screen.blit(self.surface,self.rect)


class Dark_screen(pygame.sprite.Sprite):
    def __init__(self,sleep=None,alpha=255):
        super(Dark_screen, self).__init__()
        self.height,self.width = size = pygame.display.get_window_size()
        self.surface = pygame.Surface(size,pygame.SRCALPHA)
        self.surface.fill('black')
        self.surface.set_alpha(alpha)
        self.rect = self.surface.get_rect()
        self.sleep = sleep
        self.time_ = pygame.time.get_ticks()


    def update(self,screen):
        if self.sleep is not None:
            current_time = pygame.time.get_ticks()
            if current_time - self.time_ >= self.sleep: self.kill()
        screen.blit(self.surface,self.rect)


class Load_screen(pygame.sprite.Sprite):
    def __init__(self,time=10**4,alpha=255):
        super(Load_screen, self).__init__()
        self.height,self.width = size = pygame.display.get_window_size()
        self.surface = pygame.Surface(size,pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.surface.fill('black')
        self.surface.set_alpha(alpha)
        self.time = time
        self.time_ = pygame.time.get_ticks()
        self.font = pygame.font.SysFont('sans-serif', 30)




    def update(self,screen:pygame.Surface):
        current_time = pygame.time.get_ticks()
        num = (round(current_time - self.time_)//500) % 4
        text = self.font.render(f'Загрузка{"."* num  if num !=0 else 1}',True,'white')
        text_rect = text.get_rect(bottomright=(self.height-20,self.width-20))
        if current_time - self.time_ >= self.time: self.kill()
        screen.blit(self.surface,self.rect)
        screen.blit(text,text_rect)
