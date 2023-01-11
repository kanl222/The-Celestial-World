import pygame
from support import import_csv_layout
from config import *
from player import Player
from magic import Magic
from particles import Particle
from enemy import Enemy
from save_game_system import load_saves, save
from object_ import Object_
from npc import NoPlayChatcter
from events import SETVISIBLEMOUSE
from screen_effect import Darking, Dark_screen, ScreenEffectList, Load_screen
from Item import Weapon
from upgrade import Upgrade
from pause_menu import PauseMenu
from ui import UI


class Level:
    def __init__(self, data, PlyerData=None):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.set_visible_mouse(False)
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
        self.Object_sprites = Object_()
        self.data_object = data['Object']
        self.data_magic = data['Magic']
        self.data_enemy = data['Enemy']
        self.data_npc = data['NPC']

        self.flag_pos_player = False
        if PlyerData is not None:
            self.create_player(PlyerData, data['Player'])
        else:
            self.create_player()

        # particle
        self.animation = Particle(self.data_magic)
        self.magic_player = Magic(self.animation)

        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.flag_upgrade_menu = False

        self.pause = PauseMenu()
        self.flag_pause_menu = False

    def load_map(self):

        self.layouts = {
            'boundary': import_csv_layout('../csv/floor_blocks.csv'),
            'object': import_csv_layout('../csv/object.csv'),
            'entity': import_csv_layout('../csv/entity.csv'),
            'enemy': import_csv_layout('../csv/enemy.csv')
        }

    def create_map(self):
        self.screen_effect.add(Load_screen(2000), Darking())
        for style, layout in self.layouts.items():
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
                            if col == '0' and not self.flag_pos_player:
                                self.player.change_pos((x, y))
                            elif col in self.data_npc.keys():
                                NoPlayChatcter((x, y), self.data_npc[col],
                                               [self.visible_sprites])
                        elif style == 'enemy':
                            if col in self.data_enemy.keys():
                                Enemy(
                                    self.data_enemy[col],
                                    (x, y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_number,
                                    self.trigger_death_particles,
                                    self.add_exp)
                        elif style == 'boundary':
                            if col == '0':
                                self.Object_sprites.AddStaticObject({}, (x, y), [
                                    self.obstacle_sprites])


    def create_player(self, player_info=None, data=None):
        self.player = Player(
            (0, 0),
            [self.visible_sprites],
            self.obstacle_sprites, self.create_attack,
            self.destroy_attack, self.trigger_death_player, self.create_magic,
            self.import_magic, self.upgrade_menu, self.pause_menu)
        if player_info is not None:
            self.location = ''
            self.player.player_name = player_info['name']
            self.player.load_data(data[player_info['species']], player_info['species'])
        else:
            self.load_player()
        self.load_map()
        self.create_map()

    def load_player(self):
        save_data = load_saves()
        self.flag_pos_player = True
        self.player.player_name = save_data['player']['name']
        self.player.load_data(save_data['player']['data'])
        self.player.change_pos(save_data['player']['pos'])

    def load(self):
        [sprite.kill() for sprite in self.visible_sprites]
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.create_player()

    def save(self):
        data = {"player": {
            "location": '1',
            "pos": self.player.rect.center,
            "name": self.player.player_name,
            "data": {
                "species": self.player.species,
                "character": self.player.character,
                "point_character": self.player.point_character,
                "count_money": self.player.count_money,
                "exp": self.player.exp,
                "level": self.player.level,
                "energy_recovery_coef": self.player.energy_recovery_coef,
                "xp_before_up_level": self.player.xp_before_up_level
            }
        }
        }
        save(data)

    def set_visible_mouse(self, isVisible):
        pygame.event.post(pygame.event.Event(SETVISIBLEMOUSE, isVisible=isVisible))

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.attack_sprites])

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
        self.screen_effect.add(Darking(reverse=True))

    def trigger_death_particles(self, pos, particle_type):
        self.animation.create_particles(particle_type, pos, self.visible_sprites)

    def trigger_number(self, rect, number, color):
        self.animation.create_number(rect, number, [self.visible_sprites], color)

    def add_exp(self, amount):
        self.player.exp += amount

    def upgrade_menu(self):
        self.flag_upgrade_menu = not self.flag_upgrade_menu
        self.set_visible_mouse(self.flag_upgrade_menu)

    def pause_menu(self):
        self.flag_pause_menu = not self.flag_pause_menu
        self.set_visible_mouse(self.flag_pause_menu)

    def resume(self):
        if self.flag_pause_menu: return self.pause_menu()
        if self.flag_upgrade_menu: return self.upgrade_menu()

    def create_magic(self, id_magic, type, name, cost):
        magic = {"support": {
            'heal': self.magic_player.heal},
            "attack": {
                'OnEnemyMagic': self.magic_player.OnEnemyMagic,
                'Bullet': self.magic_player.BulletMagic
            }
        }

        magic[type][name](id_magic, self.player, cost,
                          [self.visible_sprites, self.attack_sprites])

    def run(self, events):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.flag_pause_menu: return self.pause.update(events)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.visible_sprites.npc_update(self.player)
        self.player_attack_logic()
        self.death_player()
        if self.flag_upgrade_menu:  self.upgrade.update(events)
        self.screen_effect.update()


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
