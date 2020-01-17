from zero import *

class Tile:
	def __init__(self, letter=''):
		self.letter = letter
		self.directionals = {}
	def __repr__(self):
		return 'Tile({0})'.format(self.letter)

class Board:	
	def __init__(self, length, chars=''):
		if chars != '':
			assert len(chars) == length*length, 'need chars to be equal to length * length'
		self.length = length

		if chars == '':
			self.grid = [[Tile() for _ in range(length)] for _ in range(length)]
		else:
			chars_iter = iter(chars)
			self.grid = [[Tile(next(chars_iter)) for _ in range(length)] for _ in range(length)]

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

test = Board(4, 'LAPSROSETIMESOFT')

def dfs(tile):
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

def boardmaker(b, num_words, lower=3, upper=8):
	'''
	b should be a 4by4 board of empty tiles
	Manually inserts num_words number of words into an empty Board. Each word inserted
	has length lower_bound <= 'l' <= upper_bound. 'b' should be an empty grid (that is, one populated with Tiles that have letter = '')
	'''
	possible_words = list(word for word in allwords if lower <= len(word) <= upper)
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
					return False

				next_tile = random.choice(valid_tiles)

			so_far += word[0]
			path.append(tile)
			word = word[1:]
			tile = next_tile

		visited.extend(path)
		for tile in path:
			tile.letter = so_far[0]
			so_far = so_far[1:]

		return True

	def fill_empty():
		for row in b.grid:
			for tile in row:
				if tile.letter == '':
					new_letter = random.choice(commons)
					tile.letter = new_letter

	while num_words > 0:
		a = random.choice(possible_words)
		print(a)
		insert_word(a)
		num_words -= 1

	fill_empty()

def solver(b):
	valids = set()
	for row in b.grid:
		for tile in row:
			valids.update(dfs(tile))
	return valids

def updater(empty_tiles):
	for tile in empty_tiles:
		alphabet = list(string.ascii_uppercase)
		tile.letter = random.choice(alphabet)

		while alphabet != [] and dfs(tile) == set():
			alphabet.remove(tile.letter)
			tile.letter = random.choice(alphabet)

		if alphabet == []: #that letter on the tile is unable to form a word at all, so we just resort to picking a commonly used letter
			tile.letter = random.choice(commons)

		print(tile.letter, dfs(tile))
		
b = Board(8)
boardmaker(b, 12)


	

	












		


