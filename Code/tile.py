import pygame
from Sitting import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.queue = 1
		self.image = pygame.image.load('../graphics/object/1/1 (2).png').convert_alpha()
		self.image = pygame.transform.scale(self.image,
											(self.image.get_size()[0] * 2 + 32,
											 self.image.get_size()[1] *3))
		self.rect = self.image.get_rect(midbottom=pos)
		self.hitbox = self.rect.inflate(-50,-200)

	def update(self, *args, **kwargs) -> None:
		print(234)
