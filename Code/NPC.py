import pygame as pg
from Entity import Entity
from DialogSystem import DialogSystem
import json

class NoPlayChatcter(Entity):
    def __init__(self,pos,data_npc=None,groups=None):
        super().__init__(groups)
        self.sprite_type = 'npc'
        if data_npc is not None:
            self.data_npc = data_npc
            self.name = self.data_npc['Name']
            self.image = self.data_npc['Sprite']
            self.dialogs = self.import_dialog()
        else:
            self.name = 'Куб'
            self.image = pg.Surface((30, 40))
            self.image.fill('red')
        self.rect = self.image.get_rect(bottomleft=pos)
        self.dialog = DialogSystem()
        self.mes = f'{self.name}: Кто ты?'
        self.choise = {1: "Привет как дела?",2: "Ты кто",3:"Уйти"}
        self.flag_dialog_selection = False
        print(self.image.get_size(),23)


    def import_dialog(self):
            with open(f"../data/dialogs/{self.name}.json", 'r') as file_:
                file = file_.read()
                if not file:
                    return {}
                return json.loads(file)


    def shop(self):
        pass

    def quest(self):
        pass

    def npc_update(self,player):
        keys = pg.key.get_pressed()
        if player.EntityVector2().distance_to(pg.math.Vector2(self.rect.center)) <= 100:
            self.dialog.message_ = self.mes
            if keys[pg.K_SPACE]:
                player.flag_moving = False
                self.dialog.speak_ = (self.choise)
                self.mes = f'{self.name}:Как дела????'
            self.dialog.update()
