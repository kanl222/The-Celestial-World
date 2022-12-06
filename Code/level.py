import pygame
from support import import_folder_json,import_csv_layout
from Sitting import *
from tile import Tile
from Player import Player
from magic import MagicPlayer
from Particles import Animation
from Mobs import Enemy
from Weapon import Weapon
from threading import Thread
from Object.Object_ import Object

from UI import UI


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        location = 1

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.load_map()
        self.Object_sprites = Object
        self.data = import_folder_json()
        self.data_object = self.data['Object'][0]
        print(self.data_object)
        self.create_map(location)

        #particle
        self.animation = Animation(self.data['Magic'])
        self.magic_player = MagicPlayer(self.animation)

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
                            elif col in self.data_object.keys():
                                self.Object_sprites.AddStaticObject('',self.data_object[col],(x, y),[self.visible_sprites,self.obstacle_sprites])
                            else:
                                if col == '113':
                                    monster_name = 'squid'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_number,
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
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def trigger_death_particles(self, pos, particle_type):
        self.animation.create_particles(particle_type, pos, self.visible_sprites)

    def trigger_number(self,rect,number,color):
        self.animation.create_number(rect,number,[self.visible_sprites],color)

    def add_exp(self, amount):

        self.player.exp += amount

    def create_magic(self, style, strength, cost):
        magic = {"support":{
            'heal': self.magic_player.heal},
            "Attack":{
            'flame': self.magic_player.flame,
            'Magiccirle': self.magic_player.Magiccirle
            }
        }

        magic['Attack'][style](self.player, cost,[self.visible_sprites,self.attack_sprites])


    def Update_UI(self):
        self.ui.display(self.player)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        Thread(target=self.Update_UI ,daemon=True).run()
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
        self.distance_w =  self.display_surface.get_width()//2 + 160
        self.distance_h = self.display_surface.get_height() // 2 + 160
        self.offset = pygame.math.Vector2()


        # creating the floor
        self.floor_surf = pygame.image.load(
            '../graphics/level 1.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.floor_surf = pygame.transform.scale(self.floor_surf,
                                                 (self.floor_surf.get_size()[0]*3,self.floor_surf.get_size()[1]*3 ))

    def custom_draw(self, player:Player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        sprites = [sprite for sprite in self.sprites()
                if player.EntityVector2().distance_to(pygame.math.Vector2(sprite.rect.center)) <= self.distance_w
                if abs(player.EntityVector2().y - pygame.math.Vector2(sprite.rect.center).y) <= self.distance_h]
        self.count_sprite_updates = len(sprites)
        for sprite in sorted(sprites, key=lambda sprite: sprite.rect.midbottom[1]):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)



    def enemy_update(self, player:Player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'
                         if (player.EntityVector2() - sprite.EntityVector2()).magnitude() <= 500]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
            pygame.draw.rect(self.display_surface, (255, 0, 0), enemy.rect, 2)

