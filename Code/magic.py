import pygame as pg
from sitting import *
from random import randint


class Magic:
	def __init__(self,animation_player):
		self.animation_player = animation_player


	def Direction(self,player):
		if player.status.split('_')[0] == 'Right':
			return pg.math.Vector2(1, 0)
		elif player.status.split('_')[0] == 'Left':
			return pg.math.Vector2(-1, 0)
		elif player.status.split('_')[0] == 'Up':
			return pg.math.Vector2(0, -1)
		else:
			return pg.math.Vector2(0, 1)



	def heal(self,player,strength,cost,groups):
		if player.energy >= cost:
			player.add_health(strength)
			player.energy -= cost
			self.animation_player.create_particles('aura',player.rect.center,groups)
			self.animation_player.create_particles('heal',player.rect.center,groups)

	def LineMagic(self,id_magic,player,cost,groups):
		if player.energy >= cost:
			player.energy -= cost
			direction = self.Direction(player)

			for i in range(1,6):
				if direction.x: #horizontal
					offset_x = (direction.x * i) * TILESIZE
					x = player.rect.centerx + offset_x
					y = player.rect.centery + 24
					self.animation_player.create_particles(id_magic,(x,y),groups)
				else: # vertical
					offset_y = (direction.y * i) * TILESIZE
					x = player.rect.centerx
					y = player.rect.centery + offset_y
					self.animation_player.create_particles(id_magic,(x,y),groups)

	def OnEnemyMagic(self,id_magic, player, cost, groups):
		if player.energy >= cost:
			for sprite in [sprite for sprite in groups[0] if player.EntityVector2().distance_to(pg.math.Vector2(sprite.rect.center)) <= 400 if sprite.__class__.__name__ == 'Enemy']:
				if player.energy >= cost:
					player.energy -= cost
					self.animation_player.create_particles(id_magic,sprite.rect.center, groups)


	def BulletMagic(self,id_magic, player, cost, groups):
		if player.energy >= cost:
			player.energy -= cost
			self.animation_player.creat_bullet_magic(id_magic,self.Direction(player),player.rect.center,groups)








