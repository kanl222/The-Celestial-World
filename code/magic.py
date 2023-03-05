import pygame as pg
from config import *
from random import randint


class Magic:
	def __init__(self,animation_player):
		self.animation_player = animation_player


	def get_direction(self, player):
		status = player.status.split('_')[0]
		if status == 'Right':
			return pg.math.Vector2(1, 0)
		elif status == 'Left':
			return pg.math.Vector2(-1, 0)
		elif status == 'Up':
			return pg.math.Vector2(0, -1)
		else:
			return pg.math.Vector2(0, 1)

	def heal(self, player, strength, cost, groups):
		if player.energy >= cost:
			player.add_health(strength)
			player.energy -= cost
			self.animation_player.create_particles('aura', player.rect.center, groups)
			self.animation_player.create_particles('heal', player.rect.center, groups)

	def line_magic(self, id_magic, player, cost, groups):
		if player.energy >= cost:
			player.energy -= cost
			direction = self.get_direction(player)
			for i in range(1, 6):
				if direction.x:
					x = player.rect.centerx + direction.x * i * TILESIZE
					y = player.rect.centery + 24
				else:
					x = player.rect.centerx
					y = player.rect.centery + direction.y * i * TILESIZE
				self.animation_player.create_particles(id_magic, (x, y), groups)

	def on_enemy_magic(self, id_magic, player, cost, groups):
		for sprite in [sprite for sprite in groups[0] if player.EntityVector2().distance_to(pg.math.Vector2(sprite.rect.center)) <= 400 if sprite.__class__.__name__ == 'Enemy']:
			if player.energy < cost:
				break
			player.energy -= cost
			self.animation_player.create_particles(id_magic, sprite.rect.center, groups)

	def bullet_magic(self, id_magic, player, cost, groups):
		if player.energy >= cost:
			player.energy -= cost
			direction = self.get_direction(player)
			self.animation_player.creat_bullet_magic(id_magic, direction, player.rect.center, groups)








