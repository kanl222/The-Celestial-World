import pygame as pg
from entity import Entity
from DialogSystem import DialogSystem

class NoPlayChatcter(Entity):
    def __init__(self,pos,type_npc,groups):
        super().__init__(groups)
        self.sprite_type = 'npc'
        self.type_npc = type_npc
        self.name = 'Куб'
        self.image = pg.Surface((30, 40))
        self.image.fill('red')
        self.rect = self.image.get_rect(bottomleft=pos)
        self.dialog = DialogSystem()
        self.mes = f'{self.name}: Кто ты?'

    def shop(self):
        pass

    def quest(self):
        pass

    def update(self):
        pass

    def npc_update(self,player):
        keys = pg.key.get_pressed()
        if player.EntityVector2().distance_to(pg.math.Vector2(self.rect.center)) <= 100:
            self.dialog.message_ = self.mes
            if keys[pg.K_SPACE]:
                self.dialog.speak_ = (self.mes)
                self.mes = f'{self.name}:Как дела????'
            self.dialog.update()
