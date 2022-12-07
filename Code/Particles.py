import pygame
from random import choice
import pygame.freetype


class Animation:
    def __init__(self, frames):
        self.frames = frames[0]

    def reflect_images(self, frames):
        return [pygame.transform.flip(x, True, False) for x in frames]

    def create_grass_particles(self, pos, groups):
        ParticleEffect(pos, choice(self.frames['leaf']), groups)

    def create_particles(self, animation_type, pos, groups):
        ParticleEffect(pos, self.frames[animation_type]['Animation'], groups)

    def create_number(self, pos: tuple, number: int, groups: list,color=None):
        NumberRender(pos, number, groups,color)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.queue = 2
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()


class NumberRender(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, number: int,groups: list, color='white'):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.sprite_type = 'DamageIndicator'
        self.queue = 4
        self.moving_y = 0
        self.animation_speed = 0.8
        ui_font = 'Serif'
        self.font = pygame.font.SysFont(ui_font, 20,True)
        self.image = self.font.render(f'-{number}' if number > 0 else f'+{number}', True, color)
        self.rect = self.image.get_rect(midtop=(pos[0], pos[1] - 10))

    def animate(self):
        if self.moving_y < 16:
            self.rect.y -= self.animation_speed
            self.moving_y += self.animation_speed
        else:
            self.kill()

    def update(self):
        self.animate()
