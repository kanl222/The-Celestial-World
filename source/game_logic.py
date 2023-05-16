import pygame
from concurrent.futures import ThreadPoolExecutor
from support import import_csv_layout
from sprites import *
from config import *
from magic import MagicLogic,Magic
from particles import Particle
from save_game_system import load_saves, save
from object_ import ObjectGroup
from music import Music
from events import SETVISIBLEMOUSE
from screen_effect import Darking, DarkScreen, LoadScreen,ScreenEffectList
from item import Weapon,WeaponSprite
from interfaces import PauseMenu,GameOverMenu,Upgrade,UI
from level import Level

thread_pool = ThreadPoolExecutor(max_workers=1)

class GameLogic:
    def __init__(self,data,screen_effect_list:ScreenEffectList) -> None:
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # screen effect
        self.screen_effect:ScreenEffectList = screen_effect_list
        self.init_level = False

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()


        # sprite setup
        self.Object_sprites = ObjectGroup()
        self.data_object = data['Object']
        self.data_magic = data['Magic']
        self.data_enemy = data['Enemy']
        self.data_npc = data['NPC']
        self.data_player = data['Player']
        self.level_object = Level(self.data_object,self.data_npc,self.data_enemy,
                                  self.visible_sprites,self.obstacle_sprites,
                                  self.attack_sprites,self.attackable_sprites,self.screen_effect,self.Object_sprites,
                                  self.damage_player,self.trigger_number,self.trigger_death_particles,self.add_exp)

        self.music = Music()
        self.music.add_multiple_music_to_list("../music")
        self.music.change_volume(sittings["volume_music"])


        # particle
        self.animation = Particle()
        self.magic_logic = MagicLogic(self.animation)


        self.ui = UI()

        self.upgrade = Upgrade(self.data_player['character'])
        self.flag_upgrade_menu = False

        self.pause = PauseMenu()
        self.flag_pause_menu = False

        self.game_over_menu = GameOverMenu()
        self.flag_game_over_menu = False

    def init_player(self,plyer_data):
        if plyer_data is not None:
            self.create_player(plyer_data)
        else:
            self.create_player()

    


    def create_player(self, player_info=None):
        self.player = Player(
            (0, 0),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
            self.trigger_death_player,
            self.create_magic,
            self.import_magic,
            self.import_weapon,
            self.upgrade_menu,
            self.pause_menu)
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
        self.future = thread_pool.submit(self.level_object.create_map)
        self.screen_effect.add(LoadScreen(pool=self.future), Darking(end_func=lambda:self.music.play_music(self.music.music_list[0])))


    def load_player(self):
        save_data = load_saves()
        self.player.flag_pos_player = True
        self.level_object.location = save_data['player']['location']
        self.player.player_name = save_data['player']['name']
        self.player.load_data(save_data['player']['data'])
        self.player.change_pos(save_data['player']['pos'])


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

    
    def load(self):
        [sprite.kill() for sprite in self.visible_sprites]
        self.reset_game_logic()
        self.set_visible_mouse(False)
        self.create_player()

    def set_visible_mouse(self, isVisible):
        pygame.event.post(pygame.event.Event(SETVISIBLEMOUSE, isVisible=isVisible))

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_attack(self):
        self.current_attack = WeaponSprite(self.player,[self.attack_sprites])

    def player_attack_logic(self):
        try:
            if self.attack_sprites:
                for attack_sprite in self.attack_sprites:
                    collision_sprites = pygame.sprite.spritecollide(attack_sprite,
                                                                    self.attackable_sprites,
                                                                    False)
                    collision_sprites_obj = pygame.sprite.spritecollide(attack_sprite,
                                                                    self.Object_sprites,
                                                                    False)
                    if collision_sprites or collision_sprites_obj:
                        if attack_sprite.__class__.__name__ == 'Bullet':
                            attack_sprite.collision()
                        for target_sprite in collision_sprites:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                    if collision_sprites_obj:
                        if attack_sprite.__class__.__name__ == 'Bullet':
                            attack_sprite.collision()
                        for target_sprite in collision_sprites:
                            if target_sprite.__class__.__name__ == "DestructibleObjtect":
                                pass
        except Exception as e:
            print(e)


    def import_magic(self, list_id_magic:list=[]):
        return {id: Magic(self.data_magic[id],self.magic_logic) for id in list_id_magic}
    
    def import_weapon(self, list_id_weapon:list=[]):
        if list_id_weapon:
            return {id: Weapon() for id in list_id_weapon}
        return Weapon()

    def damage_player(self, damage):
        if self.player.vulnerable:
            self.player.get_damage(damage)

    def trigger_death_player(self):
        self.music.fade_music()
        self.screen_effect.add(Darking(reverse=True,end_func=self._game_over_menu))

    def trigger_death_particles(self, pos, frames):
        self.animation.create_particles(frames, pos, self.visible_sprites)

    def trigger_number(self, rect, number, color):
        self.animation.create_number(rect, number, [self.visible_sprites], color)

    def add_exp(self, amount):
        self.player.exp += amount

    def upgrade_menu(self):
        self.flag_upgrade_menu = not self.flag_upgrade_menu
        self.set_visible_mouse(self.flag_upgrade_menu)

    def pause_menu(self):
        if self.player.flag_pause_menu:
            self.flag_pause_menu = not self.flag_pause_menu
            self.set_visible_mouse(self.flag_pause_menu)

    def _game_over_menu(self):
        print(24)
        self.flag_game_over_menu = not self.flag_game_over_menu
        self.set_visible_mouse(self.flag_game_over_menu)

    def resume(self):
         return self.pause_menu()

    def create_magic(self):
        self.player.magic.create_magic(self.player,[self.visible_sprites, self.attack_sprites])

    def reset_game_logic(self):
        self.init_level = False


        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.level_object = Level(self.data_object,self.data_npc,self.data_enemy,
                                  self.visible_sprites,self.obstacle_sprites,
                                  self.attack_sprites,self.attackable_sprites,self.screen_effect,self.Object_sprites,
                                  self.damage_player,self.trigger_number,self.trigger_death_particles,self.add_exp)
        self.flag_upgrade_menu = False
        self.flag_pause_menu = False
        self.flag_game_over_menu = False
        self.player = None
        
    def run(self, events):
        if not self.future.done():
            return
        if self.flag_game_over_menu:
            return self.game_over_menu.update(events)
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        if self.flag_pause_menu:
            return self.pause.update(events)
        self.visible_sprites.update()
        with ThreadPoolExecutor() as executor:
            executor.submit(self.visible_sprites.enemy_update, self.player)
            executor.submit(self.visible_sprites.npc_update, self.player,events)
            executor.submit(self.player_attack_logic)
        if self.flag_upgrade_menu:
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

    def creating_floor(self,location):
        self.floor_surf = pygame.image.load(
            f'../maps/{location}/map.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player: 'Player') -> None:
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_position)
        sprites = [sprite for sprite in self.sprites()]


        self.count_sprite_updates = len(sprites)

        for sprite in sorted(sprites, key=lambda sprite: sprite.rect.midbottom[1]):
            sprite_offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, sprite_offset_position)

    def enemy_update(self, player: 'Player') -> None:
        enemy_sprites = (sprite for sprite in self.sprites()
                         if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy')
        for enemy in enemy_sprites:
            try:
                enemy.enemy_update(player)
            except Exception as e:
                print(e)

    def npc_update(self, player: 'Player',events) -> None:
        npc_sprites = (sprite for sprite in self.sprites()
                       if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'npc')
        for npc in npc_sprites:
            try:
                npc.npc_update(player,events)
            except Exception as e:
                print(e)


