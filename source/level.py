import pygame
from support import import_csv_layout
from sprites import *
from config import *



class Level:
    def __init__(self, data_object, data_npc, data_enemy, visible_sprites,
                 obstacle_sprites, attack_sprites, attackable_sprites, screen_effect,
                 object_sprites, damage_player, trigger_number, trigger_death_particles,
                 add_exp):
        self.player = None
        self.location = None
        self.data_object = data_object
        self.data_npc = data_npc
        self.data_enemy = data_enemy
        self.visible_sprites = visible_sprites
        self.obstacle_sprites = obstacle_sprites
        self.attack_sprites = attack_sprites
        self.attackable_sprites = attackable_sprites
        self.object_sprites = object_sprites
        self.layouts = None
        self.screen_effect = screen_effect
        self.damage_player = damage_player
        self.trigger_number = trigger_number
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

    def load_map(self):
        self.layouts = {
            'boundary': import_csv_layout(f'../maps/{self.location}/_floor_blocks.csv'),
            'object': import_csv_layout(f'../maps/{self.location}/_object.csv'),
            'entity': import_csv_layout(f'../maps/{self.location}/_entity.csv'),
            'enemy': import_csv_layout(f'../maps/{self.location}/_enemy.csv')
        }

    def create_map(self):
        try:
            for style, layout in self.layouts.items():
                for row_index, row in enumerate(layout):
                    for col_index, col in enumerate(row):
                        x, y = self._get_tile_position(row_index, col_index)
                        if style == 'object' and col in self.data_object:
                            self.create_object(self.data_object[col], x, y)
                        elif style == 'entity':
                            self._add_entity(col, x, y)
                        elif style == 'enemy' and col in self.data_enemy:
                            self.create_enemy(col, x, y)
                        elif style == 'boundary' and col == '0':
                            self.object_sprites.add_static_object({}, (x, y), [
                                self.obstacle_sprites])
        except Exception as e:
            print(e)

    def create_enemy(self, style, x, y):
        data = self.data_enemy[style]
        enemy = Enemy(data, (x, y),
                      [self.visible_sprites, self.attackable_sprites],
                      self.obstacle_sprites,
                      self.damage_player,
                      self.trigger_number,
                      self.trigger_death_particles,
                      self.add_exp)


    def create_object(self, data, x, y):
        self.object_sprites.add_static_object(data, (x, y), [
            self.visible_sprites,
            self.obstacle_sprites])

    def set_player_position(self, pos):
        self.player.change_pos(pos)

    def set_map_location(self, location):
        self.location = location

    def _add_entity(self, col, x, y):
        if col == '0' and not self.player.flag_pos_player:
            self.set_player_position((x, y))
        elif col in self.data_npc:
            Npc((x, y), self.data_npc[col], [self.visible_sprites])


    def _get_tile_position(self, row_index, col_index):
        return col_index * TILESIZE, row_index * TILESIZE

