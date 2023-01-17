import pygame
import pygame as pg
from entity import Entity
from dialog import DialogSystem
from support import import_image

class NoPlayChatcter(Entity):
    def __init__(self,pos,data_npc=None,groups=None):
        super().__init__(groups)
        self.sprite_type = 'npc'
        self.data_npc = data_npc
        self.name = self.data_npc['name']
        self.image = import_image(f'../graphics/npc/{self.name}.png')
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.dialog = DialogSystem(self.name)



    def npc_update(self,player):
        keys = pg.key.get_pressed()
        if player.EntityVector2().distance_to(self.EntityVector2()) <= 100:
            if keys[pg.K_e] and not self.dialog.flag:
                player.flag_moving = False
                self.dialog.flag = True
            if keys[pygame.K_ESCAPE] or not self.dialog.flag:
                self.dialog.flag = False
                player.flag_moving = True

            if self.dialog.flag:
                self.dialog.update()


