import random
import string

def randomchar():
	return random.choice(string.ascii_uppercase)

def load_words():
    with open('word_dictionary.txt') as word_file:
        valid_words = list(word_file.read().split())

    return valid_words

class Tile:
	empty = None

	def __init__(self, letter):
		self.letter = letter
		#directionals
		self.directionals = {'n':Tile.empty, 's':Tile.empty, 'w':Tile.empty, 'e':Tile.empty, 'nw':Tile.empty, 'ne':Tile.empty, 'sw':Tile.empty, 'se':Tile.empty}
	
	def __repr__(self):
		return 'Tile({0})'.format(self.letter)

class Board():	
	'''
	2D square grid of tiles 
	'''
	def __init__(self, length, chars=''):
		if chars != '':
			assert len(chars) == length*length, 'need chars to be equal to length * length'
		self.length = length
		self.grid = [[] for _ in range(length)]

		if chars == '':
			for i in range(length):
				for _ in range(length):
					new_tile = Tile(randomchar())
					self.grid[i].append(new_tile)
		else:
			for i in range(length):
				for _ in range(length):
					new_tile = Tile(chars[0])
					self.grid[i].append(new_tile)
					chars = chars[1:]


		for i in range(length):
			for j in range(length):
				tile = self.grid[i][j]

				if i - 1 >= 0:
					tile.directionals['n'] = self.grid[i - 1][j]
				if i + 1 < length:
					tile.directionals['s'] = self.grid[i + 1][j]
				if j - 1 >= 0:
					tile.directionals['w'] = self.grid[i][j - 1]
				if j + 1 < length:
					tile.directionals['e'] = self.grid[i][j + 1]
				if i - 1 >= 0 and j - 1 >= 0:
					tile.directionals['nw'] = self.grid[i - 1][j - 1]
				if i - 1 >= 0 and j + 1 < length:
					tile.directionals['ne'] = self.grid[i - 1][j + 1]
				if i + 1 < length and j - 1 >= 0:
					tile.directionals['sw'] = self.grid[i + 1][j - 1]
				if i + 1 < length and j + 1 < length:
					tile.directionals['se'] = self.grid[i + 1][j + 1]
			
	def __repr__(self):
		val = ''
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				val += str(self.grid[i][j]) + ' '
			val += '\n'
		return val

b = Board(4, 'LAPSROSETIMESOFT')
print(b)

allwords = load_words()

def dfs(tile, word, min_word_length=2, max_word_length=5):
	visited = []

	def helper(tile, word):
		if len(word) > max_word_length:
			return
		if tile in visited: 
			return
		if word in allwords and len(word) >= min_word_length:
			print(word)

		visited.append(tile)
		for direction in tile.directionals.values():
			if direction is not Tile.empty and direction not in visited:
				helper(direction, word + direction.letter)
		visited.remove(tile)

	helper(tile, word)

dfs(b.grid[0][0], b.grid[0][0].letter, 1)

def user(start): #start should be b.grid[x][y]
	selected_tiles = [start]
	word_so_far = start.letter
	current = start
	
	while True:
		direction = input("Enter direction: ") #n, s, w, e, nw, ne, sw, se, END

		if direction in current.directionals.keys():
			next_tile = current.directionals[direction]
			if next_tile is not None and next_tile not in selected_tiles:
				selected_tiles.append(next_tile)
				word_so_far += next_tile.letter
				current = next_tile

		elif direction == 'END':
			print(word_so_far)
			if word_so_far in allwords:
				print("WORD YOU MADE WAS IN THE ENGLISH DICTIONARY CONGRATS")
				for group in b.grid:
					for tile in selected_tiles:
						if tile in group:
							group[group.index(tile)] = None
				selected_tiles = []
				word_so_far = ''
				new_start = input("Enter new tile to start on: ")





		


