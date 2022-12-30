import pygame
from Sitting import *
from Entity import Entity
from Support import import_folder
from math import inf
from Effects import EffectsList


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack,trigger_death,
                 create_magic, import_magic):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/player/elf/Down_idle/Down.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        #self.queue = 2

        self.import_player_assets()
        self.status = 'Down'
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.obstacle_sprites = obstacle_sprites
        #magic
        self.create_magic = create_magic
        self.import_magic = import_magic
        self.magic_index = 0
        self.magic_data = self.import_magic(['2', '1'])
        self.magic_list = list(self.magic_data.keys())
        self.magic = self.magic_data[self.magic_list[self.magic_index]]
        self.can_switch_magic = True
        self.magic_switch_time = None


        self.trigger_death = trigger_death
        self.attack_magic = True
        self.attacking = False

        self.player_data()

        self.flag_moving = True
        self.vulnerable = True
        self.hurt_time = None
        self.living = True
        self.invulnerability_duration = 500

    def change_pos(self,pos):
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)


    def import_player_assets(self):
        character_path = '../graphics/player/elf/'
        self.animations = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                           'Right_idle': [], 'Left_idle': [], 'Up_idle': [],
                           'Down_idle': []
                           }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)



    def player_data(self, PlayerData=None):
        if PlayerData is None:
            self.species = "elf"
            self.character = {'Power': 5, 'Intelligence': 5, 'Physique': 5, 'Dexterity': 5}
            self.start_stats = {'health': 100, 'energy': 100, 'attack': 10, 'magic': 4,
                          'speed': 5}
            self.update_stats()
            self.upgrade_cost = {'health': 50, 'energy': 50}
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.effects_list = EffectsList()
            self.count_money = 0
            self.exp = 0
            self.level = 0
            self.energy_recovery_coef = 0.02
            self.xp_before_up_level = 100
            self.speed = self.stats['speed']
        else:
            self.stats = PlayerData['stats']
            self.max_stats = PlayerData['max_stats']
            self.upgrade_cost = PlayerData['upgrade_cost']
            self.health = self.stats['health']
            self.energy = self.stats['energy']
            self.effects_list = EffectsList()
            self.count_money = PlayerData['count_money']
            self.exp = PlayerData['exp']
            self.level = PlayerData['level']
            self.xp_before_up_level = PlayerData['xp_before_up_level']
            self.speed = self.stats['speed']

    def update_stats(self):
        health = self.start_stats['health'] + self.start_stats['energy'] * 0.02 + self.character['Physique'] * 5
        energy = self.start_stats['energy'] + self.character['Physique'] * 0.05 + self.character['Intelligence'] * 5
        attack = self.start_stats['attack'] + self.character['Physique'] * 0.05 + self.character['Power'] * 5
        magic = self.start_stats['magic'] + self.character['Intelligence'] * 5
        speed = self.start_stats['speed'] + self.character['Dexterity'] * 0.02
        self.stats = {'health': round(health), 'energy': round(energy), 'attack': round(attack), 'magic': round(magic), 'speed': round(speed)}

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'Up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'Down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'Right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'Left'
        else:
            self.direction.x = 0

        if keys[pygame.K_LCTRL]:
            if self.attack_magic:
                self.attacking = True
                self.attack_magic = False
                self.attack_time = pygame.time.get_ticks()
                type = self.magic["Type"].split('_')
                cost = self.magic["Mana"]
                self.create_magic(self.magic_list[self.magic_index], type[0], type[1],
                                  cost)

        if keys[pygame.K_1] and self.can_switch_magic:
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            self.magic_index = (self.magic_index + 1) % len(self.magic_list)
            self.magic = self.magic_data[self.magic_list[self.magic_index]]

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
        if not self.living:
            self.living = not self.living
            self.health = self.stats['health']
            self.energy = self.stats['energy']


    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def add_energy(self, strength):
        self.energy += strength
        if self.energy > self.max_stats['energy']:
            self.energy = self.max_stats['energy']

    def add_health(self, strength):
        self.health += strength
        if self.health >= self.stats['health']:
            self.health = self.stats['health']

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.magic['Cooldown']:
                self.attacking = False
                self.attack_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

    def update_level(self):
        if (self.exp - self.xp_before_up_level) >= 0:
            self.start_stats['health'] += self.upgrade_cost['health']
            self.start_stats['energy'] += self.upgrade_cost['energy']
            self.update_stats()
            self.xp_before_up_level += int(self.xp_before_up_level * 0.25)
            self.level += 1

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = self.magic['Damage']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += self.energy_recovery_coef * self.character['Intelligence']
        else:
            self.energy = self.stats['energy']

    def update(self):
        if self.flag_moving and  self.living:
            self.input()
            self.cooldowns()
            self.get_status()
            self.animate()
            self.energy_recovery()
            self.update_level()
            self.move(self.stats['speed'])
