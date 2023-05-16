import pygame as pg
from concurrent.futures import Future

class ScreenEffectList(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pg.display.get_surface()

    @property
    def sprites(self):
        return super().sprites()

    def update(self,events):
        if self.sprites:
            self.sprites[0].update(self.screen,events)

    def get_sprite(self):
        return self.sprites[0]




class Darking(pg.sprite.Sprite):
    def __init__(self, speed=4, sleep=1000, reverse=False,end_func=lambda:None,start_func=lambda:None):
        super().__init__()
        self.surface = pg.Surface(pg.display.get_window_size(), pg.SRCALPHA)
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect()
        self.time = pg.time.get_ticks()
        self.sleep = sleep
        self.speed = speed
        self.end_func = end_func
        self.start_func = start_func()
        self.flag_reverse = reverse
        self.alpha = 255 if not reverse else 0
        self.surface.set_alpha(self.alpha)

    def update(self, screen,events):
        current_time = pg.time.get_ticks()
        if current_time - self.time >= self.sleep:
            self.surface.set_alpha(self.alpha)
            if 0 <= self.alpha <= 255:
                self.alpha -= self.speed if not self.flag_reverse else -self.speed
            else:
                self.end_func()
                self.kill()
        screen.blit(self.surface, self.rect)

class DarkScreenPress(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pg.Surface(pg.display.get_window_size(), pg.SRCALPHA)
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect()
        self.time_ = pg.time.get_ticks()
        self.font = pg.font.SysFont('sans-serif', 30)

    def update(self, screen,events):
            text = self.font.render('Press Any Key to Continue', True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(self.surface, self.rect)
            screen.blit(text, text_rect)
            pg.display.flip()
            for event in events:
                if event.type == pg.KEYDOWN:
                    self.kill()
            screen.blit(self.surface, self.rect)



class DarkScreen(pg.sprite.Sprite):
    def __init__(self, sleep=None, alpha=255):
        super().__init__()
        self.surface = pg.Surface(pg.display.get_window_size(), pg.SRCALPHA)
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(alpha)
        self.rect = self.surface.get_rect()
        self.sleep = sleep
        self.time_ = pg.time.get_ticks()

    def update(self, screen,events):
        if self.sleep is not None:
            current_time = pg.time.get_ticks()
            if current_time - self.time_ >= self.sleep:
                self.kill()
        screen.blit(self.surface, self.rect)


class LoadScreen(pg.sprite.Sprite):
    def __init__(self, time=10**3, alpha=255,pool:Future=None):
        super().__init__()
        self.surface = pg.Surface(pg.display.get_window_size(), pg.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(alpha)
        self.time = time
        self.pool = pool
        self.time_ = pg.time.get_ticks()
        self.font = pg.font.SysFont('sans-serif', 30)

    def update(self, screen,events):
        current_time = pg.time.get_ticks()
        num = (round(current_time - self.time_) // 500) % 4
        text = self.font.render(f'Loading{"."*(num if num != 0 else 1)}', True, (255, 255, 255))
        text_rect = text.get_rect(bottomright=(self.rect.w - 20, self.rect.h - 20))
        if self.pool is not None:
            if self.pool.done() and current_time - self.time_ >= self.time: 
                self.kill()
        elif current_time - self.time_ >= self.time:
                self.kill()
        screen.blit(self.surface, self.rect)
        screen.blit(text, text_rect)
   
