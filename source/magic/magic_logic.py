import pygame as pg
from config import *
from random import randint
from .magic import Magic
from sprites.player import Player
from particles import ParticleEffect

class MagicLogic:
    def __init__(self, animation_player: ParticleEffect):
        self.animation_player:ParticleEffect = animation_player

    def get_direction(self, player:Player) -> pg.math.Vector2:
        status = player.status.split('_')[0]
        if status == 'Right':
            return pg.math.Vector2(1, 0)
        elif status == 'Left':
            return pg.math.Vector2(-1, 0)
        elif status == 'Up':
            return pg.math.Vector2(0, -1)
        else:
            return pg.math.Vector2(0, 1)

    def on_player(self, player: Player, magic: Magic, groups):
        if player.energy >= magic.cost:
            player.energy -= magic.cost
            player.effects.add_effect(magic.effect)
            self.animation_player.create_particles(player.rect.center, magic.animation_frame(), groups)

    def line_magic(self, player: Player, magic: Magic, groups):
        if player.energy >= magic.cost:
            player.energy -= magic.cost
            direction = self.get_direction(player)
            for i in range(1, 6):
                if direction.x:
                    x = player.rect.centerx + direction.x * i * TILESIZE
                    y = player.rect.centery + 24
                else:
                    x = player.rect.centerx
                    y = player.rect.centery + direction.y * i * TILESIZE
                self.animation_player.create_particles((x, y), magic.animation_frames(), groups)

    def area_magic(self, player: Player, magic: Magic, groups, radius: int):
        if player.energy >= magic.cost:
            player.energy -= magic.cost
            top_left_x = player.rect.centerx - TILESIZE * magic.radius
            top_left_y = player.rect.centery - TILESIZE * magic.radius
            for x in range(1,magic.radius*2):
                for y in range(1,magic.radius*2):
                    tile_rect = pg.Rect(top_left_x + x*TILESIZE, top_left_y + y*TILESIZE, TILESIZE, TILESIZE)
                    if pg.math.Vector2(tile_rect.center) <= (TILESIZE * magic.radius):
                        self.animation_player.create_particles(tile_rect.center, magic.animation_frames(), groups)



    def on_enemy_magic(self,  player: Player, magic: Magic, groups):
        for sprite in [sprite for sprite in groups[0] if player.get_position().distance_to(pg.math.Vector2(sprite.rect.center)) <= 400 if sprite.__class__.__name__ == 'Enemy']:
            if player.energy < magic.cost:
                break
            player.energy -= magic.cost
            self.animation_player.create_particles(
                magic.animation_frames(), sprite.rect.center, groups)

    def bullet_magic(self,  player: Player, magic: Magic, groups):
        if player.energy >= magic.cost:
            player.energy -= magic.cost
            direction = self.get_direction(player)
            self.animation_player.creat_bullet_magic(direction, player.rect.center,magic.animation_frames(), groups)
