from graphics import *
from first import *

width, height = 640, 640
window = GraphWin("Word Game", width, height, autoflush=False)
window.setCoords(0, 0, width, height)

'''
FOR TESTING PURPOSES. ALL OF THIS WILL BE REDONE USING PYGAME
'''
score = 0
selected = []

def drawboard(b):
	x, y = 128, 512
	for i in range(len(b.grid)):
		for j in range(len(b.grid[i])):
			b.grid[i][j].block = Rectangle(Point(x, y), Point(x + 64, y + 64)).draw(window)
			b.grid[i][j].text = Text(Point(x + 32, y + 32), b.grid[i][j].letter).draw(window)
			x += 64
		x = 128
		y -= 64
	Rectangle(Point(0, 0), Point(64, 64)).draw(window)

def clickloop(b):
	global score, selected

	pt = window.getMouse()
	for i in range(len(b.grid)):
		for j in range(len(b.grid[i])):
			tile = b.grid[i][j]
			if tile.letter != '':
				if tile.block.getP1().getX() < pt.getX() < tile.block.getP2().getX() and tile.block.getP1().getY() < pt.getY() < tile.block.getP2().getY():
					if tile not in selected and (tile in selected[-1].directionals.values() if selected else True):
						selected.append(tile)
						tile.block.setFill('green')
					elif tile is selected[-1]:
						selected.remove(tile)
						tile.block.setFill('white')
				
				elif 0 < pt.getX() < 64 and 0 < pt.getY() < 64:
					word = ''.join([tile.letter for tile in selected])
					if word in allwords:
						score += len(word)
						print("{0}: You got {1} pts!".format(word, len(word)))
						empty_tiles = []
						for used in selected:
							used.text.undraw()
							used.block.setFill('white')
							used.letter = ''
							empty_tiles.append(used)
						updater(empty_tiles)
						for tile in empty_tiles:
							tile.text = Text(tile.text.getAnchor(), tile.letter)
							tile.text.draw(window)

					else:
						for used in selected:
							used.block.setFill('white')
					selected = []

drawboard(b)

while not window.isClosed():
	clickloop(b)

		
			





