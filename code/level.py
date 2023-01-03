import pygame
from support import import_folder_json, import_csv_layout
from sitting import *
from player import Player
from magic import Magic
from particles import Particle
from enemy import Enemy
from threading import Thread
from object_ import Object_
from npc import NoPlayChatcter
from screen_effect import Darking, Dark_screen, ScreenEffectList

from ui import UI


class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # screen effect
        self.screen_effect = ScreenEffectList()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.load_map()
        self.Object_sprites = Object_()
        data = import_folder_json()
        self.data_object = data['Object']
        self.data_magic = data['Magic']
        self.data_npc = data['NPC']
        self.player = Player(
            (0, 0),
            [self.visible_sprites],
            self.obstacle_sprites, self.create_attack,
            self.destroy_attack, self.trigger_death_player, self.create_magic,
            self.import_magic)
        self.create_map()
        print(data)

        # particle
        self.animation = Particle(self.data_magic)
        self.magic_player = Magic(self.animation)

        self.ui = UI()

    def load_map(self):
        self.layouts = {
            'map': import_csv_layout('../csv/map.csv'),
            'object': import_csv_layout('../csv/object.csv'),
            'entity': import_csv_layout('../csv/entity.csv')
        }

    def create_map(self):
        for style, layout in self.layouts.items():
            if style == 'map': continue
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'object':
                            if col in self.data_object.keys():
                                self.Object_sprites.AddStaticObject(self.data_object[col],
                                                                    (x, y),
                                                                    [self.visible_sprites,
                                                                     self.obstacle_sprites])
                        elif style == 'entity':
                            if col == '0':
                                self.player.change_pos((x, y))
                            elif col in self.data_npc.keys():
                                NoPlayChatcter((x, y), self.data_npc[col],
                                               [self.visible_sprites])
                            else:
                                if col == '113':
                                    monster_name = 'slime'
                                else:
                                    monster_name = 'slime'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_number,
                                    self.trigger_death_particles,
                                    self.add_exp)
        self.screen_effect.add(Darking())

    def create_attack(self):
        self.current_attack = Weapon(self.player,
                                     [self.visible_sprites, self.attack_sprites])

    def load(self):
        [sprite.kill() for sprite in self.visible_sprites if
         sprite.__class__.__name__ != 'Player']
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.create_map()

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
                    if attack_sprite.__class__.__name__ == 'Bullet': attack_sprite.collision()
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def import_magic(self, list_id_magic):
        return {id: self.data_magic[id]['data'] for id in list_id_magic}

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.get_damage(amount)

    def death_player(self):
        if not self.screen_effect and not self.player.living:
            self.player.revival()
            self.load()

    def trigger_death_player(self):
        self.screen_effect.add(Darking(True), Dark_screen())

    def trigger_death_particles(self, pos, particle_type):
        self.animation.create_particles(particle_type, pos, self.visible_sprites)

    def trigger_number(self, rect, number, color):
        self.animation.create_number(rect, number, [self.visible_sprites], color)

    def add_exp(self, amount):
        self.player.exp += amount

    def create_magic(self, id_magic, type, name, cost):
        magic = {"support": {
            'heal': self.magic_player.heal},
            "Attack": {
                'OnEnemyMagic': self.magic_player.OnEnemyMagic,
                'Bullet': self.magic_player.BulletMagic
            }
        }

        magic[type][name](id_magic, self.player, cost,
                          [self.visible_sprites, self.attack_sprites])

    def Update_UI(self):
        self.ui.display(self.player)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.npc_update(self.player)
        self.Update_UI()
        self.player_attack_logic()
        self.death_player()
        self.screen_effect.update(self.display_surface)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.distance_w = self.display_surface.get_width() // 2 + 160
        self.distance_h = self.display_surface.get_height() // 2 + 160
        self.offset = pygame.math.Vector2()
        self.creating_floor()

        # creating the floor

    def creating_floor(self):
        self.floor_surf = pygame.image.load(
            '../graphics/level 1.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)
        sprites = [sprite for sprite in self.sprites()
                   if player.EntityVector2().distance_to(
                pygame.math.Vector2(sprite.rect.center)) <= self.distance_w
                   if abs(player.EntityVector2().y - pygame.math.Vector2(
                sprite.rect.center).y) <= self.distance_h]
        self.count_sprite_updates = len(sprites)
        for sprite in sorted(sprites, key=lambda sprite: sprite.rect.midbottom[1]):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            self.hitbox_(sprite)


    def hitbox_(self,sprite):
        try:
            pygame.draw.rect(self.display_surface, 'red', sprite.hitbox,2)
        except Exception:
            pass

    def enemy_update(self, player: Player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)



    def npc_update(self, player: Player):
        npc_sprites = [sprite for sprite in self.sprites() if
                       hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'npc']
        for npc in npc_sprites:
            npc.npc_update(player)
