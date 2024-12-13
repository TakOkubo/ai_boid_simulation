import pygame

ENEMY_POWER = 250
RADIUS_OF_ENEMY = 10

# 敵
class Enemy:
	def __init__(self, id, x, y, enemy_power=ENEMY_POWER):
		self.id = id
		self.x = x
		self.y = y
		self.power = enemy_power
		self.radius = RADIUS_OF_ENEMY
		self.clashed = False

	def move(self):
		pass

	def display(self, screen):
		pygame.draw.rect(screen, (255, 0, 0), (int(self.x), int(self.y), self.radius * 2, self.radius * 2))