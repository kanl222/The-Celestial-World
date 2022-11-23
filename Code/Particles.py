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

    def create_particles(self, animation_type, sprite, groups,sprite_type):
        ParticleEffect(sprite.rect.center,self.frames[animation_type]['Animation'], groups,sprite_type,sprite)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups,sprite_type,sprite):
        super().__init__(groups)
        self.Sprite_ = sprite
        self.queue = 2
        self.sprite_type = sprite_type
        self.frame_index = 0
        self.angle = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[int(self.frame_index)]
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)

        self.pos = pos

    def rot_center(self,image, angle):
        try:
            """rotate an image while keeping its center and size"""
            orig_rect = image.get_rect()
            rot_image = pygame.transform.rotate(image, angle)
            rot_rect = orig_rect.copy()
            rot_rect.center = rot_image.get_rect().center
            rot_image = rot_image.subsurface(rot_rect).copy()
            return rot_image
        except ValueError:
            return rot_image


    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.Sprite_.Moving = True
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def animate_rotate(self):
        self.angle += 6
        if self.angle % 360 == 0:
            self.kill()
        else:
            self.image = self.rot_center(self.orig_image,self.angle)


    def update(self):
        if self.sprite_type == 'magic_circle':
            self.animate_rotate()

        elif self.sprite_type == 'magic':
            self.animate()


