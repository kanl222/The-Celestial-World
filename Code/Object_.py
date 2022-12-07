import pygame
from ObjectSprite import *

class Object_:
    def __init__(self):
        pass

    def AddStaticObject(self,data:dict,pos:tuple,groups:list):
        StaticObject(data,pos,groups)

    def AddDestructibleObjtect(self,data:dict,pos:tuple,groups:list):
        DestructibleObjtect(data,pos,groups)

    def AddUsingObjtect(self,data:dict,pos:tuple,groups:list):
        UsingObject(data,pos,groups)




