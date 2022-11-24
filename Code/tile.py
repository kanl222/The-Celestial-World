import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.queue = 0
		self.display_surface = pygame.display.get_surface()
		self.image = pygame.image.load('../graphics/object/1/1 (2).png').convert_alpha()
		self.image = pygame.transform.scale(self.image,
											(self.image.get_size()[0] * 2 + 32,
											 self.image.get_size()[1] *3))
		self.rect = self.image.get_rect(bottomright=pos)
		self.hitbox = self.rect.inflate(-50,-10)

	def update(self, *args, **kwargs) -> None:
		self.e = pygame.draw.rect(self.display_surface, (255,255,0), self.hitbox)
