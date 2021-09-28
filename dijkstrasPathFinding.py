import pygame
pygame.init()
import pygame
width, height = 750, 750
rows, cols = 50, 50
square_size = width//cols
red = (255, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 160, 250)
gray = (128, 128, 128)
orange = (255, 165, 0)
from queue import PriorityQueue
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dijkstra,s path visualizer')
FPS = 50
class Spot:
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.x = row*square_size
		self.y = col*square_size
		self.color = white
		self.neighbours = []
	def make_blank(self):
		self.color = white
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, square_size, square_size))
	def make_start(self):
		self.color = red
	def make_end(self):
		self.color = blue
	def make_barrier(self):
		self.color = black
	def is_barrier(self):
		return self.color == black
	def make_closed(self):
		self.color = orange
	def make_open(self):
		self.color = green
	def make_path(self):
		self.color = gray 
	def get_neighbours(self, grid):
		# self.neighbours = []
		x = [1, -1, 0, 0]
		y = [0, 0, -1, 1]
		for i in range(4):
			if self.row+y[i] < rows and self.col+x[i] < cols and self.row+y[i] >= 0 and self.col+x[i] >= 0:
				if not grid[self.row+y[i]][self.col+x[i]].is_barrier():
					self.neighbours.append(grid[self.row+y[i]][self.col+x[i]])

def draw_grid(win):
	for i in range(rows):
		pygame.draw.line(win, gray, (0, i * square_size), (width, i * square_size))
		for j in range(rows):
			pygame.draw.line(win, gray, (j * square_size, 0), (j * square_size, width))
def draw(win, grid):
	for row in grid:
		for spot in row:
			spot.draw(win)

def make_grid(rows):
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j)
			grid[i].append(spot)
	return grid

def get_clicked_pos(pos):
	y, x = pos
	row = y//square_size
	col = x//square_size
	return row, col

def reconstruct(start, end, camefrom, grid, win):
	current = camefrom[end]
	while current != start:
		current.make_path()
		current = camefrom[current]
		draw(win, grid)
		draw_grid(win)
		pygame.display.update()

def dijkstra(win, start, end, grid):
	open_Set = PriorityQueue()
	count = 0
	open_Set.put((0, count, start))
	camefrom = {}
	score = {spot : float('inf') for row in grid for spot in row}
	score[start] = 0
	open_set_hash = {start}
	while not open_Set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_Set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			current.make_end()
			reconstruct(start, end, camefrom, grid, win)
			return
		if current != start:
			current.make_closed()
		for node in current.neighbours:
			if score[node] > score[current] + 1:
				score[node] = score[current] + 1
				camefrom[node] = current
				if node not in open_set_hash:
					count += 1
					open_Set.put((score[node], count, node))
					node.make_open()
					open_set_hash.add(node)
		draw(win, grid)
		draw_grid(win)
		pygame.display.update()

def main():
	run = True
	grid = make_grid(rows)
	start = None;
	clock = pygame.time.Clock()
	end = None
	while run:
		clock.tick(FPS)
		win.fill(white)
		draw(win, grid)
		draw_grid(win)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos)
				spot = grid[row][col]
				if not start:
					start = spot
					start.make_start()
				elif not end and end != start:
					end = spot
					end.make_end()
				elif spot != end and spot != start:
					spot.make_barrier()

			if pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos)
				grid[row][col].make_blank()
				if (grid[row][col] == start):
					start = None
				if (grid[row][col] == end):
					end= None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c and start and end:
					start = None
					end = None
					grid = make_grid(rows)

				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.get_neighbours(grid)
					dijkstra(win, start, end, grid)

		pygame.display.update()
	pygame.quit()
	quit()

main()