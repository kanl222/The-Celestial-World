import pygame
from Sitting import *
from random import randint


class MagicPlayer:
	def __init__(self,animation_player):
		self.animation_player = animation_player


	def Direction(self,player):
		if player.status.split('_')[0] == 'Right':
			return pygame.math.Vector2(1, 0)
		elif player.status.split('_')[0] == 'Left':
			return pygame.math.Vector2(-1, 0)
		elif player.status.split('_')[0] == 'Up':
			return pygame.math.Vector2(0, -1)
		else:
			return pygame.math.Vector2(0, 1)



	def heal(self,player,strength,cost,groups):
		if player.energy >= cost:
			player.add_health(strength)
			player.energy -= cost
			self.animation_player.create_particles('aura',player.rect.center,groups)
			self.animation_player.create_particles('heal',player.rect.center,groups)

	def flame(self,player,cost,groups):
		if player.energy >= cost:
			player.energy -= cost
			direction = self.Direction(player)

			for i in range(1,6):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x
					y = player.rect.centery + 24
					self.animation_player.create_particles('Flame',(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx
					y = player.rect.centery + offset_y
					self.animation_player.create_particles('Flame',(x,y),groups)

	def Magiccirle(self, player, cost:int, groups:list):
		if player.energy >= cost:
			for sprite in groups[0]:
				if sprite.__class__.__name__ == 'Enemy':
					player.energy -= cost
					enemy_vec = pygame.math.Vector2(sprite.rect.center)
					player_vec = pygame.math.Vector2(player.rect.center)
					if (player_vec - enemy_vec).magnitude() <= 400:
						self.animation_player.create_particles('Flamecircle',sprite.rect.center, groups)




