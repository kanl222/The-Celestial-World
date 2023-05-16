import random
import pygame
from config import *
from .entity import Entity
from support import *
from effects import EffectsList
from elemets import Damage

class Enemy(Entity):
    def __init__(self, data, pos, groups, obstacle_sprites, damage_player,trigger_damage,
                 trigger_death, add_exp):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        # graphics setup
        self.import_graphics(data['name'])
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = data['name']
        self.level = 1
        monster_info = data
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death
        self.trigger_render_number = trigger_damage
        self.add_exp = add_exp

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.ignore_notice_radius = False
        self.invincibility_duration = 300

        self.effects = EffectsList(self)



    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_distance_direction(self, pos):
        enemy_vec = self.get_position()
        player_vec = pygame.math.Vector2(pos)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        distance = self.get_distance_direction(player.rect.center)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
            self.ignore_notice_radius = False
        elif distance <= self.notice_radius or self.ignore_notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(Damage(self.attack_damage, self.attack_type))
        elif self.status == 'move':
            self.direction = self.get_distance_direction(player.rect.center)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def info_enemy_up(self):
        self.font = pygame.font.SysFont('Serif', 2, True)
        self.text = self.font.render(f'{self.monster_name} Lv:{self.level}', True,
                                      'red')
        self.rect_text = self.image.get_rect(midtop=(self.rect.midtop[0], self.rect.midtop[1] + 20))
        self.image.blit(self.text,self.rect_text)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_distance_direction(player.rect.center)[1]
            if attack_type == 'weapon':
                damage_class = player.get_full_weapon_damage()
                damage_class.apply_damage(self)
            else:
                damage_class = player.get_full_magic_damage()
                damage_class.apply_damage(self)
            self.trigger_render_number(self.rect.midtop,str(-damage_class.amount),'red')
            self.hit_time = pygame.time.get_ticks()
            self.ignore_notice_radius = True
            self.vulnerable = False
    
    def get_damage_effect(self,damage_class):
        damage_class.apply_damage(self)
        self.trigger_render_number(self.rect.midtop,str(-damage_class.amount),'red')

    def check_death(self):
        if self.health <= 0:
            self.kill()
            # self.trigger_death_particles(self.rect.center, self.monster_name)
            self.trigger_render_number(self.rect.midtop, str(self.exp), 'green')
            self.add_exp(self.exp)

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.effects.update_effects()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
