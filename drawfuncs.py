from graphics import *
from base import * 

window = GraphWin("WordFinder", 768, 768, autoflush=False)
window.setCoords(0, 0, 768, 768)
bg_color = 'white'
window.setBackground(bg_color)

def drawtext(text, size=24, font='helvetica'):
	text.setFace(font)
	text.setSize(size)
	text.draw(window)
	return text

def drawblock(block):
	block.setWidth(3)
	block.draw(window)
	return block

def drawboard(b):
	'''
	Draw the blocks and letters representing each tile. Each tile is randomly assigned a score 
	value from 1 to 10; different scores result in different colored tile outlines. 
	'''
	x, y = 78, 608  

	for i in range(len(b.grid)):
		for j in range(len(b.grid[i])):
			b.grid[i][j].block = drawblock(Rectangle(Point(x, y), Point(x + 64, y + 64)))
			b.grid[i][j].text = drawtext(Text(Point(x + 32, y + 32), b.grid[i][j].letter))
			b.grid[i][j].score = min(random.choice(range(1, 11)), random.choice(range(1, 11)))
			x += 78
		x = 78
		y -= 76

	for i in range(len(b.grid)):
		for j in range(len(b.grid[i])): 
			tile = b.grid[i][j]
			if 4 <= tile.score <= 5:
				tile.block.setOutline('blue')
			elif 6 <= tile.score <= 8:
				tile.block.setWidth(4)
				tile.block.setOutline('purple')
			elif 9 <= tile.score <= 10:
				tile.block.setWidth(4)
				tile.block.setOutline('yellow')
			scoretext = Text(Point(tile.block.getCenter().getX(), tile.block.getCenter().getY() - 16), str(tile.score))
			scoretext.setSize(16)
			scoretext.setFace('courier')
			scoretext.draw(window)










	

		
			





