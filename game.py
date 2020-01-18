from drawfuncs import *

b = Board(8)
attempts = 50
score = 0
previous_scores = []
selected = []

def update_score(increment=0, word=''):
	'''
	Updates the score after the player finds a word, and undraws the previous scores/increments. Draws the updated
	information. 
	'''
	for display in previous_scores:
		display.undraw()

	global score
	score = score + increment
	score_display = Text(Point(384, 736), str(score))
	drawtext(score_display, 32, 'helvetica')
	previous_scores.append(score_display)

	if increment > 0:
		increment_display = Text(Point(448, 700), '+ ' + str(increment))
		drawtext(increment_display, 16, 'courier')
		previous_scores.append(increment_display)
	
	if word:
		word_display = Text(Point(320, 700), word)
		drawtext(word_display, 20, 'courier')
		previous_scores.append(word_display)	

boardmaker(b, 15)
drawboard(b)
update_score()
attempts_text = drawtext(Text(Point(384, 48), "Attempts left: " + str(attempts)))

'''
Gameloop:

Player may start on any tile, and can then attempt to build a valid word by traversing through adjacent
tiles not already pathed through. They can also click the last tile they selected to deselect it.

Clicking outside the Board will either submit the path traversed so far, updating the score if it formed a valid word
or deselecting the whole path if no word was formed. Score is calculated based on the path's Tiles' cumulative score
values multiplied by the max(1, (length of the word - 3)). 

The player has 50 attempts: submitting a valid word decrements attempt. Game is over at 0 attempts. 
'''
while attempts > 0:
	pt = window.getMouse()

	for i in range(len(b.grid)):
		for j in range(len(b.grid[i])):
			tile = b.grid[i][j]

			if tile.letter != '':
				if tile.block.getP1().getX() < pt.getX() < tile.block.getP2().getX() and tile.block.getP1().getY() < pt.getY() < tile.block.getP2().getY():
					if tile not in selected and (tile in selected[-1].valid_directionals if selected else True):
						selected.append(tile)
						tile.block.setFill('gray')
					
					elif tile is selected[-1]:
						selected.remove(tile)
						tile.block.setFill(bg_color)
				
				elif (pt.getX() < 80 or pt.getX() > 676) or (pt.getY() < 76 or pt.getY() > 672):
					word = ''.join([tile.letter for tile in selected])
					
					if word in allwords:
						add_this = sum([tile.score for tile in selected]) * max(1, len(selected) - 3) 
						update_score(add_this, word)
						
						empty_tiles = []
						for used in selected:
							used.text.undraw()
							used.block.setFill(bg_color)
							used.letter = ''
							empty_tiles.append(used)
						tile_updater(empty_tiles)
						
						for tile in empty_tiles:
							tile.text = Text(tile.text.getAnchor(), tile.letter)
							drawtext(tile.text)
						
						attempts_text.undraw()
						attempts -= 1
						if attempts > 0:
							attempts_text = drawtext(Text(Point(384, 48), "Attempts left: " + str(attempts)))
					
					else:
						for used in selected:
							used.block.setFill(bg_color)
					
					selected = []

drawtext(Text(Point(384, 48), "Final score: " + str(score)))
window.getMouse()

