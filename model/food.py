import pygame

FOOD_POWER = 150
RADIUS_OF_FOOD = 10

# 餌
class Food:
	def __init__(self, id, x, y, food_power=FOOD_POWER):
		self.id = id
		self.x = x
		self.y = y
		self.power = food_power
		self.radius = RADIUS_OF_FOOD
		self.eaten = False

	def move(self):
		pass

	def display(self, screen):
		pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), self.radius)