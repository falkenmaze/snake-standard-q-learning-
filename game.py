import pygame
import random
from enum import Enum
import numpy as np
pygame.init()
class Direction(Enum):
	RIGHT = 1
	LEFT = 2 
	UP = 3 
	DOWN = 4
Block = 20
Speed = 10
class Game:
	def __init__(self, width=200, height=200):
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.clock = pygame.time.Clock()
		self.game_over = False
		self.reset()

	def reset(self):
		self.direction = Direction.RIGHT
		self.head = [self.width/2, self.height/2]
		self.snake = [self.head, [self.head[0] - Block, self.head[1]], [self.head[0] - Block, self.head[1]]]
		self.score = 0
		self.food = None
		self.game_over = False
		self.place_food()
		self.frameiter = 0 

	def place_food(self):
		x = random.randint(0, (self.width-Block)//Block) * Block
		y = random.randint(0, (self.height-Block)//Block) * Block
		self.food = [x,y]
		if self.food in self.snake:
			self.place_food()

	def update_ui(self):
		self.screen.fill((0,0,0))
		for pt in self.snake:
			pygame.draw.rect(self.screen, (0,255,0), pygame.Rect(pt[0], pt[1], Block, Block))
		pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(self.food[0], self.food[1], Block, Block))
		pygame.display.flip()

	def move(self, action):
		clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
		idx = clock_wise.index(self.direction)
		action = list(action)
		if np.array_equal(action, [1,0,0]):
			new_dir = clock_wise[idx]
		elif np.array_equal(action, [0,1,0]):
			nxt_idx = (idx + 1) % 4  
			new_dir = clock_wise[nxt_idx]
		else:
			nxt_idx = (idx - 1) % 4 
			new_dir = clock_wise[nxt_idx]
		self.direction = new_dir
		x = self.head[0]
		y = self.head[1]
		if self.direction == Direction.RIGHT:
			x += Block
		if self.direction == Direction.LEFT:
			x -= Block
		if self.direction == Direction.UP:
			y -= Block
		if self.direction == Direction.DOWN:
			y += Block 
		self.head = [x,y]

	def collision(self, pt=None):
		if pt == None:
			if self.head[0] > self.width - Block or self.head[0] < 0 or self.head[1] > self.height - Block or self.head[1] < 0:
				return True 
			if self.head in self.snake[1:]:
				return True
		else:
			if pt[0] > self.width - Block or pt[0] < 0 or pt[1] > self.height - Block or pt[1] < 0:
				return True 
			if pt in self.snake[1:]:
				return True

		return False

	def play(self,action):
		self.frameiter += 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			# if event.type == pygame.KEYDOWN:
			# 	if event.key == pygame.K_LEFT:
			# 		self.direction = Direction.LEFT
			# 	elif event.key == pygame.K_RIGHT:
			# 		self.direction = Direction.RIGHT
			# 	elif event.key == pygame.K_UP:
			# 		self.direction = Direction.UP
			# 	elif event.key == pygame.K_DOWN:
			# 		self.direction = Direction.DOWN
		self.move(action)
		self.snake.insert(0, self.head)
		reward = 0
		if self.collision() or self.frameiter > 100*len(self.snake):
			self.game_over = True 
			reward += -1050
			self.reset()
			return reward,self.game_over, self.score
		if self.head == self.food:
			self.score += 1
			self.place_food()
			reward += 1000
		else:
			self.snake.pop()
		self.update_ui()
		self.clock.tick(Speed)
		return reward,self.game_over, self.score