import pygame
from particles import Bullet
from save_game_system import load_saves, save
from events import SETVISIBLEMOUSE
from screen_effect import Darking, LoadScreen
from item import Weapon, WeaponSprite
from magic import Magic

class CombatManager:
    """Управляет боевой системой: атаками, уроном, коллизиями оружия и снарядов."""
    def __init__(self, game_logic):
        self.gl = game_logic
        
    def create_attack(self):
        self.gl.current_attack = WeaponSprite(self.gl.player, [self.gl.attack_sprites])

    def destroy_attack(self):
        if self.gl.current_attack:
            self.gl.current_attack.kill()
        self.gl.current_attack = None

    def damage_player(self, damage):
        if self.gl.player and self.gl.player.vulnerable:
            self.gl.player.get_damage(damage)

    def player_attack_logic(self) -> None:
        """Обрабатывает коллизии атак игрока с противниками и объектами."""
        if not self.gl.attack_sprites:
            return
        for attack_sprite in self.gl.attack_sprites:
            collision_sprites = pygame.sprite.spritecollide(
                attack_sprite, self.gl.attackable_sprites, False)
            collision_sprites_obj = pygame.sprite.spritecollide(
                attack_sprite, self.gl.Object_sprites, False)

            # Если пуля что-то задела — уничтожаем её один раз
            if (collision_sprites or collision_sprites_obj) and isinstance(
                    attack_sprite, Bullet):
                attack_sprite.collision()

            # Наносим урон противникам
            for target_sprite in collision_sprites:
                target_sprite.get_damage(self.gl.player, attack_sprite.sprite_type)

            # Наносим урон разрушаемым объектам
            for target_sprite in collision_sprites_obj:
                if hasattr(target_sprite, 'get_damage'):
                    target_sprite.get_damage(self.gl.player, attack_sprite.sprite_type)


class GameStateManager:
    """Менеджер состояний игры: отвечает за меню паузы, прокачки и экран смерти."""
    def __init__(self, game_logic):
        self.gl = game_logic
        self.flag_upgrade_menu = False
        self.flag_pause_menu = False
        self.flag_game_over_menu = False

    def set_visible_mouse(self, isVisible):
        pygame.event.post(pygame.event.Event(SETVISIBLEMOUSE, isVisible=isVisible))

    def upgrade_menu(self):
        self.flag_upgrade_menu = not self.flag_upgrade_menu
        self.set_visible_mouse(self.flag_upgrade_menu)

    def pause_menu(self):
        if self.gl.player and self.gl.player.flag_pause_menu:
            self.flag_pause_menu = not self.flag_pause_menu
            self.set_visible_mouse(self.flag_pause_menu)

    def game_over_menu(self):
        self.flag_game_over_menu = not self.flag_game_over_menu
        self.set_visible_mouse(self.flag_game_over_menu)

    def resume(self):
        self.pause_menu()

    def reset(self):
        self.flag_upgrade_menu = False
        self.flag_pause_menu = False
        self.flag_game_over_menu = False


class PlayerManager:
    """Отвечает за инициализацию, сохранение и загрузку игрока."""
    def __init__(self, game_logic):
        self.gl = game_logic

    def save(self) -> None:
        """Сохраняет текущее состояние игры."""
        if not self.gl.player: return
        data = {"player": {
            "location": self.gl.level_object.location,
            "pos": self.gl.player.rect.center,
            "name": self.gl.player.player_name,
            "data": {
                "species": self.gl.player.species,
                "character": self.gl.player.character,
                "point_character": self.gl.player.point_character,
                "count_money": self.gl.player.count_money,
                "exp": self.gl.player.exp,
                "level": self.gl.player.level,
                "energy_recovery_coef": self.gl.player.energy_recovery_coef,
                "xp_before_up_level": self.gl.player.xp_before_up_level
            }
        }}
        save(data)

    def load(self):
        [sprite.kill() for sprite in self.gl.visible_sprites]
        self.gl.reset_game_logic()
        self.gl.state.set_visible_mouse(False)
        self.gl.create_player()

    def add_exp(self, amount):
        if self.gl.player:
            self.gl.player.exp += amount

    def import_magic(self, list_id_magic: list = []):
        return {id: Magic(self.gl.data_magic[id], self.gl.magic_logic) for id in list_id_magic}

    def import_weapon(self, list_id_weapon: list = []):
        if list_id_weapon:
            return {id: Weapon() for id in list_id_weapon}
        return Weapon()
