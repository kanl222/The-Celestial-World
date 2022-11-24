import pygame
from support import import_folder_json,import_csv_layout
from Sitting import *
from tile import Tile
from Player import Player
from debug import debug
from magic import MagicPlayer
from Particles import AnimationPlayer
from Mobs import Enemy
from random import randint
from Weapon import Weapon
from threading import Thread

import sys
from UI import UI


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.ParticleEffect_sprites = ParticleEffectGroup()
        location = 1

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.load_map()
        self.create_map(location)
        self.data = import_folder_json()

        #particle
        self.animation_player = AnimationPlayer(self.data['Magic'])
        self.magic_player = MagicPlayer(self.animation_player)

        self.ui = UI()

    def load_map(self):
        self.layouts = {
            'map': import_csv_layout('../csv/map.csv'),
            'object': import_csv_layout('../csv/object.csv')
        }



    def create_map(self,location):
        for style, layout in self.layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'object':
                            if col == '108':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,self.create_attack,self.destroy_attack,self.create_magic)
                            elif col in [str(i) for i in range(203,206)]:
                                Tile((x, y),[self.visible_sprites, self.obstacle_sprites])
                            else:
                                if col == '113':
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])

    def delete_map(self):
        for sprite in self.obstacle_sprites:
            if sprite.__class__ != 'Player':
                sprite.kill()
        location = 2
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map(location)

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,
                                                                self.attackable_sprites,
                                                                False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(pos - offset,
                                                                             [
                                                                                 self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,
                                                     attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):

        self.player.exp += amount

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost,
                                    [self.ParticleEffect_sprites,[]])

        if style == 'Magiccirle':
            self.magic_player.Magiccirle(self.player, cost,
                                    [self.visible_sprites,[]]
                                         ,self.visible_sprites.sprites())


    def Update_UI(self):
        self.ui.display(self.player)

    def run(self):
        Thread(target=self.visible_sprites.custom_draw, args=(self.player,)).run()
        Thread(target=self.Update_UI, args=()).run()
        self.ParticleEffect_sprites.update()
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(
            '../graphics/level 1.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.floor_surf = pygame.transform.scale(self.floor_surf,
                                                 (self.floor_surf.get_size()[0]*3,self.floor_surf.get_size()[1]*3 ))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: (sprite.queue,player.rect.center)):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)


class ParticleEffectGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def update(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.center)