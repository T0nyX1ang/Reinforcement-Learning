import random
import json

class TTTGame(object):
	def __init__(self):
		self._board = [0] * 9
		self._end = False
		with open('learning.json', 'r') as f:
			self._state = json.loads(f.read())
		self._alpha = 0.05

	def judge(self, state):
		if (sum(state[0: 3]) == 3 or \
			sum(state[3: 6]) == 3 or \
			sum(state[6::]) == 3 or \
			sum(state[0::3]) == 3 or \
			sum(state[1::3]) == 3 or \
			sum(state[2::3]) == 3 or \
			sum(state[0::4]) == 3 or \
			sum(state[2:7:2]) == 3):
			self._end = True
			return 1
		elif (sum(state[0: 3]) == -3 or \
			sum(state[3: 6]) == -3 or \
			sum(state[6::]) == -3 or \
			sum(state[0::3]) == -3 or \
			sum(state[1::3]) == -3 or \
			sum(state[2::3]) == -3 or \
			sum(state[0::4]) == -3 or \
			sum(state[2:7:2]) == -3):
			self._end = True
			return 0
		elif 0 not in state:
			self._end = True
			return 0.5 # can be set to 0 if you need sharper winning criterion.
		else:
			self._end = False
			if str(state) not in self._state:
				self._state[str(state)] = 0.5 # move state
			return self._state[str(state)] # study starts from here ...

	def random_move(self, move_type=-1):
		self.judge(self._board)
		if (self._end):
			return '[End]'
		empty = []
		count = 0
		for val in self._board:
			if (val == 0):
				empty.append(count)
			count += 1
		select = empty[random.randint(0, len(empty) - 1)]
		move_board = self._board.copy()
		move_board[select] = move_type
		value = self.judge(move_board)
		self._state[str(self._board)] = self._state[str(self._board)] + self._alpha * (value - self._state[str(self._board)]) # update move	
		self._board = move_board.copy()
		return select

	def greedy_move(self, move_type=1):
		self.judge(self._board)
		if (self._end):
			return '[End]'
		selects = []
		max_value = -1
		count = 0
		for val in self._board:
			if (val == 0):
				move_board = self._board.copy()
				move_board[count] = move_type
				value = self.judge(move_board)
				if (value > max_value):
					selects = [count]
					max_value = value
				elif (value == max_value):
					selects.append(count)
			count += 1
		select = random.sample(selects, 1)[0]
		move_board = self._board.copy()
		move_board[select] = move_type
		value = self.judge(move_board)
		self._state[str(self._board)] = self._state[str(self._board)] + self._alpha * (value - self._state[str(self._board)]) # update move	
		self._board = move_board.copy()
		return select		

	def play(self):
		self._board = [0] * 9
		self._end = False
		while not self._end:
			s1 = self.greedy_move()
			s2 = self.random_move()
			# print('greedy selection:', s1, 'random selection:', s2)

	def train(self, epoch=1000):
		for i in range(0, epoch):
			self.play()

	def dump_state(self):
		with open('learning.json', 'w') as f:
			f.write(json.dumps(self._state))

	def pretty_print_board(self):
		print(self._board[0], self._board[1], self._board[2])
		print(self._board[3], self._board[4], self._board[5])
		print(self._board[6], self._board[7], self._board[8])

	def combat(self):
		self._board = [0] * 9
		self._end = False
		while not self._end:
			s1 = self.greedy_move()
			self.pretty_print_board()
			print("Winning prob:", self.judge(self._board))
			if (self._end):
				print('You lose / a tie!')
				break
			s2 = input('Please enter your move: ')
			while self._board[int(s2)] != 0:
				s2 = input('Please enter your move: ')
			self._board[int(s2)] = -1
			self.pretty_print_board()
			print("Winning prob:", self.judge(self._board))
			self.judge(self._board)
			if (self._end):
				print('You win!')


if __name__ == '__main__':
	tttg = TTTGame()
	tttg.combat()
	tttg.train(100000)
	tttg.dump_state()

