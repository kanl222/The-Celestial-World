import pygame as pg
from entity import Entity

class NoPlayChatcter(Entity):
    def __init__(self,groups,type_npc):
        super().__init__(groups)
        self.type_npc = type_npc


    def shop(self):
        pass

    def dialog(self):
        pass

    def quest(self):
        pass
