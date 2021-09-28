import pygame
from queue import PriorityQueue
import math
#priority queue is awesome
pygame.init()
from pathfinding.constants import maze, width, height, square_size, cols, rows, black, blue, orange, white, red, green, gray
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('a star')
start = end = wall = False
startPos = []
endPos = []
wallPos = []
FPS = 60
make_open_list = []
make_close_list = []
make_path_list = []


def square_pos(pos):
	x, y = pos
	row = y//square_size
	col = x//square_size
	return row, col

def grid():
	win.fill(white)
	for row in range(rows):
		pygame.draw.line(win, black, (0, row*square_size), (width, row*square_size), 1)

	for col in range(cols):
		pygame.draw.line(win, black, (col*square_size, 0), (col*square_size, height), 1)	

	if start:
		pygame.draw.rect(win, orange, (startPos[0][1]*square_size, startPos[0][0]*square_size, square_size, square_size))	

	if end:
		pygame.draw.rect(win, blue, (endPos[1]*square_size, endPos[0]*square_size, square_size, square_size))	
	
	if wall:
		for i in wallPos:
			pygame.draw.rect(win, black, (i[1]*square_size, i[0]*square_size, square_size, square_size))

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	#return abs(x2-x1) + abs(y2-y1)
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def neighbours():
	neighbour_dict = {}
	for row in range(rows):
		for col in range(cols):
			if 0 <= row < rows and 0 <= col < cols and maze[row][col] != 'block':
				neighbour_dict[(row, col)] = []
				if col+1 < cols and maze[row][col+1] != 'block':
					neighbour_dict[(row, col)].append([row, col+1])
				if col-1 >= 0 and maze[row][col-1] != 'block':
					neighbour_dict[(row, col)].append([row, col-1])
				if row+1 < rows and maze[row+1][col] != 'block':
					neighbour_dict[(row, col)].append([row+1, col])
				if row-1 >= 0 and maze[row-1][col] != 'block':
					neighbour_dict[(row, col)].append([row-1, col])	
	return neighbour_dict						

def make_open(list0):
	make_open_list.append(list0)

def make_close(list1):
	make_close_list.append(list1)

def make_path(list2):
	make_path_list.append(list2)

def reconstruct_path(came_from, current):
	while tuple(current) in came_from:
		current = came_from[tuple(current)]
		make_path(current)

def pathfinding():
	srow, scol = startPos[0][0], startPos[0][1]
	erow, ecol = endPos[0], endPos[1]
	count = 0
	neighbour_dict = neighbours()
	open_set = PriorityQueue()
	open_set.put((0, count, startPos[0]))
	came_from = {}
	g_score = dict.fromkeys(neighbour_dict, float('inf'))
	g_score[(srow, scol)] = 0
	f_score = dict.fromkeys(neighbour_dict, float('inf'))
	f_score[(srow, scol)] = h((srow, scol), (erow, ecol))
	
	open_set_hash = {(srow, scol)}
	clock = pygame.time.Clock()	
	while not open_set.empty():
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		current = open_set.get()[2]	
		open_set_hash.remove(tuple(current))	

		if current == endPos:
			reconstruct_path(came_from, current)
			return True		

		for neighbour in neighbour_dict[tuple(current)]:
			temp_g_score = g_score[tuple(current)] + 1

			if temp_g_score < g_score[tuple(neighbour)]:
				came_from[tuple(neighbour)] = tuple(current)
				g_score[tuple(neighbour)] = temp_g_score
				f_score[tuple(neighbour)] = temp_g_score + h(tuple(neighbour), (erow, ecol))
				if tuple(neighbour) not in open_set_hash:
					count += 1
					open_set.put((f_score[tuple(neighbour)], count, neighbour))
					open_set_hash.add(tuple(neighbour))
					make_open(neighbour)

		grid()
		for li in make_open_list:
			if len(li) != 0:
				pygame.draw.rect(win, green, (li[1]*square_size, li[0]*square_size, square_size, square_size))

		for lj in make_close_list:
			if len(lj) != 0:
				pygame.draw.rect(win, red, (lj[1]*square_size, lj[0]*square_size, square_size, square_size))			

		if current != startPos[0]:
			make_close(current)	

		pygame.display.update()	

def reset():
	for row in range(rows):
		for col in range(cols):
			maze[row][col] = 0
	make_open_list.clear()
	make_close_list.clear()
	make_path_list.clear()
	start, end, wall = False, False, False
	startPos.clear()
	endPos.clear()
	wallPos.clear()
	pygame.display.update()	
	main()

def main():
	run = True
	hold = False
	clock = pygame.time.Clock()		
	global start, end, startPos, endPos, wall 
	while run:

		clock.tick(FPS)

		grid()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pathfinding()	

				if event.key == pygame.K_r:
					reset()	

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:	
				if len(startPos) == 0:
					pos = pygame.mouse.get_pos()
					row, col = square_pos(pos)
					start = True
					startPos.append([row, col])
					maze[startPos[0][0]][startPos[0][1]] = 'start'

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:	
				pos = pygame.mouse.get_pos()
				row, col = square_pos(pos)
				end = True
				endPos = [row, col]	
				maze[endPos[0]][endPos[1]] = 'end'

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				wall = True
				hold = True

			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				hold = False	
		if hold:
			pos = pygame.mouse.get_pos()
			row, col = square_pos(pos)	
			if maze[row][col] != 'start' and maze[row][col] != 'end' and maze[row][col] != 'block':
				maze[row][col] = 'block'
				wallPos.append([row, col])
		for li in make_open_list:
			if len(li) != 0:
				pygame.draw.rect(win, green, (li[1]*square_size, li[0]*square_size, square_size, square_size))

		for lj in make_close_list:
			if len(lj) != 0:
				pygame.draw.rect(win, red, (lj[1]*square_size, lj[0]*square_size, square_size, square_size))
		for lp in make_path_list:
			if len(lp) != 0:
				pygame.draw.rect(win, gray, (lp[1]*square_size, lp[0]*square_size, square_size, square_size))				


		pygame.display.update()		
	pygame.quit()
	quit()		

main()
