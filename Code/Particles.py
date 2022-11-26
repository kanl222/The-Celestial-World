import time

import pygame
from support import import_folder,import_folder_base64_Animation
from random import choice
import json
import base64
import io

class AnimationPlayer:
    def __init__(self,frames):
        self.frames = frames[0]


    def reflect_images(self, frames):
        return [pygame.transform.flip(x, True, False) for x in frames]

    def create_grass_particles(self, pos, groups):
        ParticleEffect(pos, choice(self.frames['leaf']), groups)

    def create_particles(self, animation_type, pos, groups):
        ParticleEffect(pos,self.frames[animation_type]['Animation'], groups)


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


class Animation:
    def create_damage_indicator(self, sprite,damage:int,groups:list):
        DamageIndicator(sprite,damage,groups)


class DamageIndicator(pygame.sprite.Sprite):
    def __init__(self, sprite,damage:int,groups:list):
        super().__init__(groups)
        self.sprite_type = 'DamageIndicator'
        self.queue = 2
        self.animation_speed = 1
        self.move_y = 0
        ui_font = 'Serif'
        font = pygame.font.Font(None, 30)
        self.image = pygame.font.SysFont(ui_font, 16).render(str(-damage), True, 'red')
        x,y = sprite.rect.midtop
        self.rect = self.image.get_rect(midtop=(x,y-10))

    def animate(self):
        if self.move_y <= 14:
            self.rect.y -= self.animation_speed
            self.move_y += self.animation_speed
        else:
            self.kill()

    def update(self):
        self.animate()
