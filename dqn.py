import numpy as np
from game import Game, Direction
import random
import pickle
avail_actions = [(1,0,0), (0,1,0), (0,0,1)]
q_table = {}
with open("q_table.dat", "rb") as f:
	q_table = pickle.load(f)

def init(q_table, state):
	if q_table.get(state) == None:
		q_table[state] = {action: 0 for action in avail_actions}
	return q_table


def get_state(game):
	head = game.snake[0]
	pl = [head[0] - 20, head[1]]
	pr = [head[0] + 20, head[1]]
	pu = [head[0], head[1] - 20]
	pd = [head[0], head[1] + 20]
	dl = game.direction == Direction.LEFT
	dr = game.direction == Direction.RIGHT
	du = game.direction == Direction.UP 
	dd = game.direction == Direction.DOWN

	state = (
		(dr and game.collision(pr))or
		(dl and game.collision(pl))or 
		(du and game.collision(pu))or 
		(dd and game.collision(pd)),

		(du and game.collision(pr))or 
		(dd and game.collision(pl))or 
		(dl and game.collision(pu))or 
		(dr and game.collision(pd)),

		(dd and game.collision(pr))or 
		(du and game.collision(pl))or 
		(dr and game.collision(pu))or 
		(dl and game.collision(pd)),

		dl,
		dr,
		du,
		dd,
		game.food[0] > game.head[0],
		game.food[0] < game.head[0],
		game.food[1] > game.head[1],
		game.food[1] < game.food[1]
		)
	state1 = np.array(state, dtype=int)
	state = ""
	for i in state1:
		state += str(i) 
	return state



def choose_action(q_table,state, epsilon):
	if random.uniform(0,1) < epsilon:
		epsilon -= 0.01
		return random.choice(avail_actions)
	else:
		return max(q_table[state], key=q_table[state].get)

def exploitation(q_table, state):
	return max(q_table[state], key=q_table[state].get)

def update_q_value(state, action, reward, next_state, lr, gamma):
	curr_q_value = q_table[state][action] 
	next_q_value = max(q_table[next_state].values())
	updated_q_value = curr_q_value + lr * (reward + gamma * next_q_value - curr_q_value)
	q_table[state][action]  = updated_q_value

game = Game()
while True:
	for i in range(150):
		game_over = game.game_over
		score = 0
		if not game_over:
			state = get_state(game)
			q_table = init(q_table, state)
			action = choose_action(q_table, state, 0.2)
			reward,game_over,score = game.play(action)
			next_state = get_state(game)
			q_table = init(q_table, next_state)
			update_q_value(state, action, reward, next_state, 0.1, 0.9)
		if i % 10 == 0:
			with open("q_table.dat", "wb") as f:
				pickle.dump(q_table, f)
			# print(score)

