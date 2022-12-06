import pygame
class Object:
    def __init__(self):
        pass

    def AddStaticObject(self,data:dict,pos:tuple,groups:list):
        print(data,pos,groups)
        StaticObject(data,pos,groups)

    def AddDestructibleObjtect(self,data,pos,groups):
        DestructibleObjtect(data,pos,groups)

    def AddUsingObjtect(self,data,pos,groups):
        UsingObject(data,pos,groups)





class DestructibleObjtect(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['Sprite']
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_size()[0] * 2 + 32,
                                             self.image.get_size()[1] * 3))
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(-40, -170)
        self.hitbox.midbottom = self.rect.midbottom



class StaticObject(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['Sprite']
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_size()[0] * 2 + 32,
                                             self.image.get_size()[1] * 3))
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(-40, -170)
        self.hitbox.midbottom = self.rect.midbottom
        print(123)


class UsingObject(pygame.sprite.Sprite):
    def __init__(self,data, pos, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.image = data['Sprite']
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_size()[0] * 2 + 32,
                                             self.image.get_size()[1] * 3))
        self.rect = self.image.get_rect(bottomleft=pos)
        self.hitbox = self.rect.inflate(-40, -170)
        self.hitbox.midbottom = self.rect.midbottom



