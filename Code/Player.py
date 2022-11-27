import pygame
from Sitting import *
from entity import Entity
from support import import_folder
from math import inf

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/player/Down_idle/Down_ (1).png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.queue = 2

        self.import_player_assets()
        self.status = 'Down'

        self.obstacle_sprites = obstacle_sprites

        self.create_magic = create_magic
        self.magic_index = -1
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        self.attack_magic = True
        self.attacking = False

        self.stats = {'health': 100, 'energy': 300, 'attack': 10, 'magic': 4, 'speed': 5}
        self.max_stats = {'health': 100, 'energy': 300, 'attack': 20, 'magic': 10,
                          'speed': 10}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic': 100,
                             'speed': 100}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.buff_damage = []
        self.buff_health = []
        self.buff_energy = [100]
        self.exp = 0
        self.level = 0
        self.xp_before_up_level = 100
        self.speed = self.stats['speed']

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        character_path = '../graphics/player/'
        self.animations = {'Up': [], 'Down': [], 'Left': [], 'Right': [],
                           'Right_idle': [], 'Left_idle': [], 'Up_idle': [],
                           'Down_idle': []
                           }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)


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
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength']

                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)

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
        self.image = pygame.transform.scale(self.image,
                                                 (self.image.get_size()[0] * 3,
                                                  self.image.get_size()[1] * 3))

    def add_energy(self,strength):
        self.energy += strength
        if self.energy > self.max_stats['energy']:
            self.energy = self.max_stats['energy']

    def add_health(self,strength):
        self.health += strength
        if self.health >= self.stats['health']:
            self.health = self.stats['health']

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= magic_data[self.magic]['cooldown']:
                self.attacking = False
                self.attack_magic = True


        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def update_level(self):
        while (self.exp - self.xp_before_up_level) >= 0:
            self.level += 1
            self.stats['health'] += self.upgrade_cost['health']
            self.stats['energy'] += self.upgrade_cost['energy']
            self.xp_before_up_level += int(self.xp_before_up_level * 0.25)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']


    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']


    def update(self):
        self.update_level()
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])