import pygame
import pygame as pg
from entity import Entity
from dialog_system import DialogSystem

class NoPlayChatcter(Entity):
    def __init__(self,pos,data_npc=None,groups=None):
        super().__init__(groups)
        self.sprite_type = 'npc'
        if data_npc is not None:
            self.data_npc = data_npc
            self.name = self.data_npc['Name']
            self.image = self.data_npc['Sprite']
        else:
            self.name = 'Куб'
            self.image = pg.Surface((30, 40))
            self.image.fill('red')
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.dialog = DialogSystem(self.name)
        self.flag_dialog_selection = False


    def shop(self):
        pass

    def quest(self):
        pass

    def npc_update(self,player):
        keys = pg.key.get_pressed()
        if player.EntityVector2().distance_to(pg.math.Vector2(self.rect.center)) <= 100:
            self.dialog.update()
            if keys[pg.K_SPACE]:
                player.flag_moving = False
                self.flag_dialog_selection = True
            if keys[pygame.K_ESCAPE] and self.flag_dialog_selection:
                player.flag_moving = True
