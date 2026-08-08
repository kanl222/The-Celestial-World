import pygame
from support import import_csv_layout, import_image
from sprites import *
from config import *
from magic import MagicLogic, Magic
from particles import Particle, Bullet
from save_game_system import load_saves, save
from object_ import ObjectGroup
from music import Music
from events import SETVISIBLEMOUSE
from screen_effect import Darking, DarkScreen, LoadScreen,ScreenEffectList
from item import Weapon,WeaponSprite
from interfaces import PauseMenu,GameOverMenu,Upgrade,UI
from level import Level

from managers import CombatManager, GameStateManager, PlayerManager

class GameLogic:
    """Главный класс логики (Фасад), который делегирует работу под-менеджерам."""
    def __init__(self,data,screen_effect_list:ScreenEffectList) -> None:
        self.display_surface = pygame.display.get_surface()
        self.screen_effect:ScreenEffectList = screen_effect_list
        self.init_level = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.Object_sprites = ObjectGroup()
        
        self.data_object = data['Object']
        self.data_magic = data['Magic']
        self.data_enemy = data['Enemy']
        self.data_npc = data['NPC']
        self.data_player = data['Player']
        
        self.player = None

        # Инициализация подсистем (Менеджеров)
        self.combat = CombatManager(self)
        self.state = GameStateManager(self)
        self.player_mgr = PlayerManager(self)

        self.level_object = Level(self.data_object,self.data_npc,self.data_enemy,
                                  self.visible_sprites,self.obstacle_sprites,
                                  self.attack_sprites,self.attackable_sprites,self.screen_effect,self.Object_sprites,
                                  self.enemy_sprites,self.npc_sprites,
                                  self.combat.damage_player,self.trigger_number,self.trigger_death_particles,self.player_mgr.add_exp)

        self.music = Music()
        self.music.add_multiple_music_to_list("music")
        self.music.change_volume(sittings["volume_music"])

        self.animation = Particle()
        self.magic_logic = MagicLogic(self.animation)

        self.ui = UI()
        self.upgrade = Upgrade(self.data_player['character'])
        self.pause = PauseMenu()
        self.game_over_menu = GameOverMenu()

        from concurrent.futures import ThreadPoolExecutor
        self._thread_pool = ThreadPoolExecutor(max_workers=1)

    def init_player(self, player_data):
        self.create_player(player_data)

    def create_player(self, player_info=None):
        self.player = Player(
            (0, 0),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.combat.create_attack,
            self.combat.destroy_attack,
            self.trigger_death_player,
            self.create_magic,
            self.player_mgr.import_magic,
            self.player_mgr.import_weapon,
            self.state.upgrade_menu,
            self.state.pause_menu)
        
        if player_info is not None:
            self.level_object.location = 1
            self.player.player_name = player_info['name']
            self.player.load_data(self.data_player[player_info['species']], player_info['species'])
        else:
            self.load_player()
            
        self.upgrade.init_player(self.player)
        self.visible_sprites.creating_floor(self.level_object.location)
        self.level_object.player = self.player
        self.level_object.load_map()
        self.future = self._thread_pool.submit(self.level_object.create_map)
        self.screen_effect.add(LoadScreen(pool=self.future), Darking(end_func=lambda:self.music.play_music(self.music.music_list[0])))

    def load_player(self):
        save_data = load_saves()
        self.player.flag_pos_player = True
        self.level_object.location = save_data['player']['location']
        self.player.player_name = save_data['player']['name']
        self.player.load_data(save_data['player']['data'])
        self.player.change_pos(save_data['player']['pos'])

    # Делегаты для внешнего вызова (из main.py и других)
    def save(self):
        self.player_mgr.save()

    def load(self):
        self.player_mgr.load()

    def resume(self):
        self.state.resume()

    def create_magic(self):
        self.player.magic.create_magic(self.player,[self.visible_sprites, self.attack_sprites])

    def trigger_death_player(self):
        self.music.fade_music()
        self.screen_effect.add(Darking(reverse=True,end_func=self.state.game_over_menu))

    def trigger_death_particles(self, pos, frames):
        self.animation.create_particles(frames, pos, self.visible_sprites)

    def trigger_number(self, rect, number, color):
        self.animation.create_number(rect, number, [self.visible_sprites], color)

    def reset_game_logic(self) -> None:
        self.init_level = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.Object_sprites = ObjectGroup()

        self.level_object = Level(self.data_object, self.data_npc, self.data_enemy,
                                  self.visible_sprites, self.obstacle_sprites,
                                  self.attack_sprites, self.attackable_sprites, self.screen_effect, self.Object_sprites,
                                  self.enemy_sprites, self.npc_sprites,
                                  self.combat.damage_player, self.trigger_number, self.trigger_death_particles, self.player_mgr.add_exp)
        
        self.state.reset()
        self.player = None
        
    def run(self, events: list) -> None:
        if not self.future.done():
            return
        if self.player is None:
            return
        if self.state.flag_game_over_menu:
            self.game_over_menu.update(events)
            return

        # Централизованная обработка ввода для взаимодействия (NPC)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for npc in self.npc_sprites.sprites():
                        if not npc.check_distance(self.player):
                            npc.interact(self.player)
                elif event.key == pygame.K_ESCAPE:
                    for npc in self.npc_sprites.sprites():
                        npc.force_end_dialog(self.player)
            
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        if self.state.flag_pause_menu:
            self.pause.update(events)
            return
            
        # Обновление всех спрайтов
        self.visible_sprites.update()
        
        # Обновление ИИ
        for enemy in self.enemy_sprites.sprites():
            enemy.enemy_update(self.player)
            
        # Обновление диалогов (events больше не передаем)
        for npc in self.npc_sprites.sprites():
            npc.npc_update(self.player)
        
        self.combat.player_attack_logic()
        
        if self.state.flag_upgrade_menu:
            self.upgrade.update(events)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.distance_w = self.display_surface.get_width() // 2 + 160
        self.distance_h = self.display_surface.get_height() // 2 + 160
        self.offset = pygame.math.Vector2()

    def add(self, *sprites):
        super().add(*sprites)

    def remove(self, *sprites):
        super().remove(*sprites)

    def empty(self):
        super().empty()

    def creating_floor(self, location):
        from support import import_image 
        self.floor_surf = import_image(f'maps/{location}/map.png')
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0)) if self.floor_surf else pygame.Rect(0, 0, 0, 0)

    def custom_draw(self, player: 'Player') -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        if self.floor_surf:
            floor_offset_pos = self.floor_rect.topleft - self.offset
            self.display_surface.blit(self.floor_surf, floor_offset_pos)

        view_rect = pygame.Rect(self.offset.x - 160, self.offset.y - 160, 
                                self.display_surface.get_width() + 320, 
                                self.display_surface.get_height() + 320)

        valid_sprites = [s for s in self.sprites() if getattr(s, 'rect', None) is not None and s.rect.colliderect(view_rect)]
        
        for sprite in sorted(valid_sprites, key=lambda s: s.rect.midbottom[1]):
            self.display_surface.blit(sprite.image, sprite.rect.topleft - self.offset)
