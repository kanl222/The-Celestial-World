import pygame
import config
from entity import Entity
from support import import_folder
#from math import inf
from effects import EffectsList


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack,
                 trigger_death,
                 create_magic, import_magic, upgrade_menu, pause_menu):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/player/elf/Down_idle/Down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -40)
        self.hitbox.midbottom = self.rect.midbottom
        self.direction = pygame.math.Vector2()

        self.player_name = ''

        self.status = 'Down'

        self.destroy_attack = destroy_attack
        self.create_attack = create_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.attack_time_weapon = None
        self.attacking_weapon = False

        self.obstacle_sprites = obstacle_sprites
        # magic
        self.create_magic = create_magic
        self.import_magic = import_magic
        self.magic_index = 0
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.attacking_magic = False
        self.attack_time_magic = None
        self.trigger_death = trigger_death

        self.flag_moving = True
        self.vulnerable = True
        self.hurt_time = None
        self.living = True
        self.invulnerability_duration = 500

        self.upgrade_menu = upgrade_menu
        self.flag_upgrade_menu = False
        self.can_upgrade_menu = True
        self.open_upgrade_menu_time = None

        self.pause_menu = pause_menu
        self.flag_pause_menu = False
        self.can_pause_menu = True
        self.open_pause_menu_time = None

        self.switch_duration_cooldown = 200

    def change_pos(self, pos):
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -30)

    def load_magic(self):
        self.magic_data = self.import_magic(['2', '1'])
        self.magic_list = list(self.magic_data.keys())
        self.magic = self.magic_data[self.magic_list[self.magic_index]]

    def import_player_assets(self):
        character_path = f'../graphics/player/{self.species}/'
        self.animations = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                           'Right_idle': [], 'Left_idle': [], 'Up_idle': [],
                           'Down_idle': [], 'Left_attack': [], 'Down_attack': [],
                           'Up_attack': [], 'Right_attack': []
                           }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)

    def load_data(self, PlayerData, species=None):
        self.species = PlayerData['species'] if species is None else species
        self.character = PlayerData['character']
        self.point_character = PlayerData['point_character']
        self.update_stats()
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.effects = EffectsList()
        self.count_money = PlayerData['count_money']
        self.exp = PlayerData['exp']
        self.level = PlayerData['level']
        self.energy_recovery_coef = PlayerData['energy_recovery_coef']
        self.xp_before_up_level = PlayerData['xp_before_up_level']
        self.speed = self.stats['speed']

        # self.list_magic = self.stats['list_magic']
        self.weapon = {'cooldown': 100, 'damage': 15}
        self.load_magic()
        self.import_player_assets()

    def update_stats(self):
        health = self.character['health'] * 20 + self.character['energy'] * 2 + \
                 self.character['body_type'] * 5
        energy = self.character['energy'] * 20 + self.character['body_type'] * 0.05 + \
                 self.character['intelligence'] * 5
        attack = self.character['body_type'] * 0.05 + self.character['dexterity'] * 0.02 + \
                 self.character['power'] * 5
        magic = self.character['intelligence'] * 5
        self.stats = {'health': round(health), 'energy': round(energy),
                      'attack': round(attack), 'magic': round(magic), 'speed': 5}

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.flag_moving or not self.living:
            self.direction = pygame.math.Vector2()
            return
        if keys[config.sittings['button_move_up']]:
            self.direction.y = -1
            self.status = 'Up'
        elif keys[config.sittings['button_move_down']]:
            self.direction.y = 1
            self.status = 'Down'
        else:
            self.direction.y = 0

        if keys[config.sittings['button_move_right']]:
            self.direction.x = 1
            self.status = 'Right'
        elif keys[config.sittings['button_move_left']]:
            self.direction.x = -1
            self.status = 'Left'
        else:
            self.direction.x = 0

        if keys[config.sittings['button_using_magic']] and not self.attacking_magic:
            self.attacking_magic = True
            self.attack_time_magic = pygame.time.get_ticks()
            type = self.magic["type"].split('_')
            cost = self.magic["cost"]
            self.create_magic(self.magic_list[self.magic_index], type[0], type[1],
                              cost)
        if keys[config.sittings['button_using_weapon']] and not self.attacking_weapon:
            self.attacking_weapon = True
            self.attack_time_weapon = pygame.time.get_ticks()
            self.create_attack()

        if keys[config.sittings['button_change_magic']] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            self.magic_index = (self.magic_index + 1) % len(self.magic_list)
            self.magic = self.magic_data[self.magic_list[self.magic_index]]

        if (keys[config.sittings['button_open_menu_upgrade']] and self.can_upgrade_menu) or (
                self.flag_upgrade_menu and keys[pygame.K_ESCAPE]):
            self.flag_upgrade_menu = not self.flag_upgrade_menu
            self.can_upgrade_menu = False
            self.open_upgrade_menu_time = pygame.time.get_ticks()
            self.upgrade_menu()

        if keys[pygame.K_ESCAPE] and self.can_pause_menu:

            self.flag_pause_menu = not self.flag_pause_menu
            self.can_pause_menu = False
            self.open_pause_menu_time = pygame.time.get_ticks()
            self.pause_menu()

    def get_damage(self, amount):
        if self.vulnerable and self.living:
            self.health -= amount
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()
            if self.health <= 0:
                self.health = 0
                self.living = False
                self.trigger_death()

    def revival(self):
        self.living = not self.living

    def get_status(self):

        # idle status
        if (self.direction.x == 0 and self.direction.y == 0) or not self.living:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking_weapon:
            self.direction = pygame.math.Vector2()
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status and int(self.frame_index + self.animation_speed) % len(self.animations[self.status]) == 0:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index = (self.frame_index + self.animation_speed) % len(animation)
        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def add_energy(self, strength):
        self.energy += strength
        if self.energy > self.stats['energy']:
            self.energy = self.stats['energy']

    def add_health(self, strength):
        self.health += strength
        if self.health >= self.stats['health']:
            self.health = self.stats['health']

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking_magic:
            if current_time - self.attack_time_magic >= self.magic['cooldown']:
                self.attacking_magic = False

        if self.attacking_weapon:
            if current_time - self.attack_time_weapon >= self.weapon['cooldown']:
                self.attacking_weapon = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.can_upgrade_menu:
            if current_time - self.open_upgrade_menu_time >= self.switch_duration_cooldown:
                self.can_upgrade_menu = True

        if not self.can_pause_menu:
            if current_time - self.open_pause_menu_time >= self.switch_duration_cooldown:
                self.can_pause_menu = True

    def up_level(self):
        if (self.exp - self.xp_before_up_level) >= 0:
            self.point_character += 2
            self.update_stats()
            self.xp_before_up_level += int(self.xp_before_up_level * 0.25)
            self.level += 1

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        spell_damage = self.weapon['damage']
        return base_damage + spell_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = self.magic['damage']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += self.energy_recovery_coef * self.character['intelligence']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.energy_recovery()
        self.up_level()
        self.move(self.stats['speed'])
