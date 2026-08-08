import random
import pygame
import math
from config import *
from .entity import Entity
from support import *
from effects import EffectsList
from elemets import Damage

class Enemy(Entity):
    def __init__(self, data, pos, groups, obstacle_sprites, damage_player, trigger_damage,
                 trigger_death, add_exp, pathfinder=None):

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
        self.max_health = monster_info['health']
        self.health = self.max_health
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

        # AI State Machine variables
        self.state = 'idle'
        self.spawn_pos = pygame.math.Vector2(pos)
        self.wander_target = None
        self.wander_timer = 0
        self.wander_duration = 0
        self.wander_cooldown = pygame.time.get_ticks()

        # Pathfinding variables
        self.pathfinder = pathfinder
        self.path = []
        self.last_path_calc_time = 0
        self.path_calc_cooldown = 1000  # Пересчитываем путь не чаще 1 раза в секунду





    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'graphics/monsters/{name}/'
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

    def alert_allies(self, player) -> None:
        """Зовет на помощь находящихся поблизости монстров в радиусе 300 пикселей."""
        if not self.groups():
            return
        for sprite in self.groups()[0]:
            if (hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy' 
                    and sprite != self and not sprite.ignore_notice_radius):
                dist = (sprite.get_position() - self.get_position()).magnitude()
                if dist <= 300:
                    sprite.ignore_notice_radius = True

    def get_status(self, player):
        distance, direction = self.get_distance_direction(player.rect.center)
        current_time = pygame.time.get_ticks()

        # 1. Отступаем, если мало здоровья (меньше 20%) и игрок близко
        if self.health < self.max_health * 0.2 and distance < self.notice_radius:
            self.state = 'retreat'
            self.ignore_notice_radius = False
            return

        # 2. Атакуем, если в радиусе атаки
        if distance <= self.attack_radius and self.can_attack:
            if self.state != 'attack':
                self.frame_index = 0
            self.state = 'attack'
            self.ignore_notice_radius = False
            self.alert_allies(player)

        # 3. Преследуем, если игрок замечен
        elif distance <= self.notice_radius or self.ignore_notice_radius:
            self.state = 'chase'
            self.alert_allies(player)

        # 4. Пассивное состояние: покой или блуждание
        else:
            self.ignore_notice_radius = False
            
            if self.state in ['chase', 'attack', 'retreat']:
                self.state = 'idle'
                self.direction = pygame.math.Vector2()
                self.wander_cooldown = current_time + random.randint(1000, 3000)

            if self.state == 'idle':
                if current_time >= self.wander_cooldown:
                    angle = random.uniform(0, 2 * math.pi)
                    dist = random.uniform(50, 150)
                    self.wander_target = self.spawn_pos + pygame.math.Vector2(math.cos(angle) * dist, math.sin(angle) * dist)
                    self.state = 'wander'
                    self.wander_timer = current_time
                    self.wander_duration = random.randint(1000, 2500)
            
            elif self.state == 'wander':
                if not self.wander_target:
                    self.state = 'idle'
                    return
                dist_to_target = (self.get_position() - self.wander_target).magnitude()
                if current_time - self.wander_timer >= self.wander_duration or dist_to_target < 10:
                    self.state = 'idle'
                    self.direction = pygame.math.Vector2()
                    self.wander_cooldown = current_time + random.randint(2000, 5000)

    def actions(self, player):
        current_time = pygame.time.get_ticks()

        if self.state == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(Damage(self.attack_damage, self.attack_type))
            self.direction = pygame.math.Vector2()
        elif self.state == 'chase':
            # Использование A* поиска пути
            if self.pathfinder:
                # Пересчитываем путь по таймауту или если пути нет
                if not self.path or current_time - self.last_path_calc_time >= self.path_calc_cooldown:
                    self.path = self.pathfinder.find_path(self.get_position(), player.rect.center)
                    self.last_path_calc_time = current_time

                if self.path:
                    # Проверяем близость к следующему узлу пути
                    next_node = self.path[0]
                    dist_to_node = (pygame.math.Vector2(next_node) - self.get_position()).magnitude()
                    
                    if dist_to_node < 35:  # Увеличено с 16 для предотвращения застреваний у стен
                        self.path.pop(0)
                        if self.path:
                            next_node = self.path[0]
                        else:
                            next_node = None

                    if next_node:
                        to_node = pygame.math.Vector2(next_node) - self.get_position()
                        if to_node.magnitude() > 0:
                            self.direction = to_node.normalize()
                        else:
                            self.direction = pygame.math.Vector2()
                    else:
                        # Если дошли до конца пути, но все еще гонимся, идем прямо на игрока
                        self.direction = self.get_distance_direction(player.rect.center)[1]
                else:
                    # Если путь не найден (стена или ошибка), идем напрямую к игроку
                    self.direction = self.get_distance_direction(player.rect.center)[1]
            else:
                self.direction = self.get_distance_direction(player.rect.center)[1]

        elif self.state == 'retreat':
            self.direction = -self.get_distance_direction(player.rect.center)[1]
        elif self.state == 'wander':
            if self.wander_target:
                to_target = self.wander_target - self.get_position()
                if to_target.magnitude() > 0:
                    self.direction = to_target.normalize()
                else:
                    self.direction = pygame.math.Vector2()
        else:
            self.direction = pygame.math.Vector2()


    def animate(self) -> None:
        """Cменяет фрейм анимации. convert_alpha() не вызывается — уже выполнено при загрузке."""
        # Сопоставляем внутреннее состояние ИИ со статусом анимаций ('idle', 'move', 'attack')
        if self.state in ['chase', 'retreat', 'wander']:
            self.status = 'move'
        else:
            self.status = self.state

        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    # Шрифт названия врага — создаётся один раз на весь класс
    _name_font = None

    def info_enemy_up(self) -> None:
        """Oтрисовывает имя и уровень врага над спрайтом."""
        if Enemy._name_font is None:
            Enemy._name_font = pygame.font.SysFont('Serif', 12, True)
        text = Enemy._name_font.render(
            f'{self.monster_name} Lv:{self.level}', True, 'red')
        rect_text = text.get_rect(midtop=(self.rect.midtop[0], self.rect.midtop[1] - 4))
        self.image.blit(text, rect_text)

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
