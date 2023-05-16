import pygame as pg
from .entity import Entity
from dialog import DialogSystem
from support import import_image


class Npc(Entity):
    def __init__(self, pos: tuple, data_npc: dict, groups: list):
        super().__init__(groups)
        self.sprite_type = 'npc'
        self.data_npc = data_npc
        self.name = self.data_npc['name']
        self.image = import_image(f'../graphics/npc/{self.name}.png')
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.dialog = DialogSystem(self.name)
        self.is_talking = False

    def start_dialog(self, player) -> None:
        player.flag_moving = False
        self.dialog.flag = True
        self.is_talking = True

    def end_dialog(self, player) -> None:
        player.flag_moving = True
        self.dialog.flag = False
        self.is_talking = False

    def npc_update(self, player, events) -> None:
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e and not self.dialog.flag and not self.check_distance(player):
                    self.start_dialog(player)
                elif event.key == pg.K_ESCAPE or not self.dialog.flag:
                    self.end_dialog(player)
        if self.dialog.flag and self.check_distance(player):
            self.end_dialog(player)
        if self.dialog.flag:self.dialog.update()

    def check_distance(self, player) -> bool:
        return player.get_position().distance_to(self.get_position()) >= 200

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self.image, self.rect)

    def handle_interaction(self, player) -> None:
        if not self.is_talking and self.check_distance(player):
            self.start_dialog(player)
        elif self.is_talking:
            self.end_dialog(player)
