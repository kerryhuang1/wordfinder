import random
import string

with open('word_dictionary.txt') as word_file:
    allwords = set(word_file.read().split())

min_dfs_length, max_dfs_length = 2, 10  

possible_dfs_words = set(word for word in allwords if min_dfs_length <= len(word) <= max_dfs_length)
valid_dfs_prefixes = set(word[:size] for word in possible_dfs_words for size in range(1, len(word)))

commons = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'R', 'D', 'H', 'U']

class Tile:
	def __init__(self, letter=''):
		self.letter = letter
		self.directionals = {}
	def __repr__(self):
		return 'Tile({0})'.format(self.letter)

class Board:
	'''
	Setting randomized to True when initializing a Board will make it much more difficult to find words
	than using boardmaker.
	'''	
	def __init__(self, length, randomized=False):
		self.length = length

		if randomized:
			self.grid = [[Tile(random.choice(list(string.ascii_uppercase))) for _ in range(length)] for _ in range(length)]
		else:
			self.grid = [[Tile() for _ in range(length)] for _ in range(length)]

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

				tile.valid_directionals = set(tile.directionals.values())
			
	def __repr__(self):
		val = ''
		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				val += str(self.grid[i][j]) + ' '
			val += '\n'
		return val

def dfs(tile):
	'''
	Set based depth-first search algorithm. Checks valid directionals recursively until 
	max_dfs_length is reached, adding every word found up to max_dfs_length to stored in the process
	Return a set containing all the words found by performing dfs on the given tile. 
	'''
	visited = set()
	stored = set()

	def helper(tile, word):
		if tile.letter == '':
			return 

		if word in possible_dfs_words:
			stored.add(word)

		if len(word) <= max_dfs_length:
			visited.add(tile)
			for direction in tile.valid_directionals - visited:
				candidate = word + direction.letter
				if candidate in valid_dfs_prefixes:
					helper(direction, candidate)
			visited.remove(tile)

	helper(tile, tile.letter)
	return stored

def boardmaker(b, num_words, lower=4, upper=10):
	'''
	Manually inserts num_words number of words into an empty Board. Each word inserted
	has length lower_bound <= 'l' <= upper_bound. 'b' should be an empty grid 
	(that is, one populated with Tiles that have letter = '').

	The words are chosen randomly and thus it is incredibly unlikely for every Tile to be filled
	with a letter from within one of the chosen words. Such leftover Tiles will have their letter
	attributes set to a random, commonly used letter. 
	'''
	possible_words = [word for word in allwords if lower <= len(word) <= upper]
	visited = []

	def find_start():
		available_tiles = [t for row in b.grid for t in row if t not in visited]
		
		if available_tiles:
			return random.choice(available_tiles)

	def insert_word(word):
		path = []
		so_far = ''
		tile = find_start()

		while word: 
			valid_tiles = list(tile.valid_directionals)
			next_tile = random.choice(valid_tiles)

			while next_tile in path or next_tile in visited:
				valid_tiles.remove(next_tile)
				if valid_tiles == []:
					return 
				next_tile = random.choice(valid_tiles)

			so_far += word[0]
			path.append(tile)
			word = word[1:]
			tile = next_tile

		for tile in path:
			tile.letter = so_far[0]
			so_far = so_far[1:]

		visited.extend(path)

	def fill_empty():
		for row in b.grid:
			for tile in row:
				if tile.letter == '':
					new_letter = random.choice(commons)
					tile.letter = new_letter

	while num_words > 0:
		insert_word(random.choice(possible_words))
		num_words -= 1

	fill_empty()

def tile_updater(empty_tiles):
	'''
	After a valid word is found, reset the tiles composing its path, using dfs to make
	sure the new tiles form valid words. In the exceptional cases that a new tile cannot,
	set its letter to a random, commonly-used letter.
	'''
	for tile in empty_tiles:
		alphabet = list(string.ascii_uppercase)

		while alphabet != [] and not dfs(tile):
			tile.letter = random.choice(alphabet)
			alphabet.remove(tile.letter)

		if alphabet == []: 
			tile.letter = random.choice(commons)

		#print(tile, dfs(tile)) UNCOMMENT THIS LINE TO PRINT POSSIBLE WORDS AFTER EACH RESET

def show_all(b, length=0):
	'''
	Return a set of all the valid words able to be formed from each tile on the board, by default.
	Specifying length will return a set of all valid words with given length.
	'''
	valids = set()
	for row in b.grid:
		for tile in row:
			valids.update(dfs(tile))
	
	if length > 0:
		return set(valid for valid in valids if len(valid) == length)
	else:
		return valids




	

	












		


