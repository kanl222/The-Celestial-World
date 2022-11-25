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
        self.angle = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)

        self.pos = pos

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()

