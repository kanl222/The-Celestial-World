import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.queue = 0
		self.display_surface = pygame.display.get_surface()
		self.image = pygame.image.load(
			'../graphics/object/1/1 (2).png').convert_alpha()
		self.image = pygame.transform.scale(self.image,
											(self.image.get_size()[0] * 2 + 32,
											 self.image.get_size()[1] *3))
		self.rect = self.image.get_rect(bottomleft=pos)
		self.hitbox = self.rect.inflate(-40,-170)
		self.hitbox.midbottom = self.rect.midbottom
