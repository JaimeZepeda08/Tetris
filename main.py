import pygame 
import random
import time

WIDTH, HEIGHT = 600, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

GREY_1 = [150, 150, 160]
GREY_2 = [90, 90, 100]
GREY_3 = [120, 120, 130]

BLUE = [51, 153, 255]
YELLOW = [215, 215, 0]
GREEN = [51, 204, 51]
PURPLE = [148, 25, 245]
ORANGE = [215, 102, 20]
RED = [215, 41, 0] 
DARK_BLUE = [40, 91, 193]

class Grid:
	def __init__(self):
		self.cols = 10
		self.rows = 20 
		self.space_size = 30

		self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]

		self.piece_colors = {0: GREY_3, 1: BLUE, 2: YELLOW, 3: GREEN, 4: PURPLE, 5: ORANGE, 6: RED, 7: DARK_BLUE}

		self.next_piece = [random.choice([L_1(), L_2(), I(), N(), T(), S_1(), S_2()]), random.choice([L_1(), L_2(), I(), N(), T(), S_1(), S_2()]), random.choice([L_1(), L_2(), I(), N(), T(), S_1(), S_2()])]
		self.curr_piece = random.choice([L_1(), L_2(), I(), N(), T(), S_1(), S_2()])
		self.pieces = [[0 for col in range(self.cols)] for row in range(self.rows)]
		self.held = None

		self.time_between = 0.5 
		self.score = 0
		self.lines_cleared = 0

	def get_grid(self):
		return self.grid

	def get_current_piece(self):
		return self.curr_piece

	def update_pieces(self):
		if not self.curr_piece.can_move(self.grid, "down"):
			for row in range(self.rows):
				for col in range(self.cols):
					if row == self.curr_piece.get_pos()[0] and col == self.curr_piece.get_pos()[1]:
						for i in range(len(self.curr_piece.get_rotation())):
							for j in range(len(self.curr_piece.get_rotation()[0])):
								new_row = row + i
								new_col = col + j
								if new_row < len(self.pieces) and new_col < len(self.pieces[0]):
									if self.curr_piece.get_rotation()[i][j] != 0:
										self.pieces[new_row][new_col] = self.curr_piece.get_rotation()[i][j]
			self.spawn_piece()

		if self.curr_piece.can_move(self.grid, "down"):
			self.curr_piece.move(self.grid, "down")

	def spawn_piece(self):
		self.curr_piece = self.next_piece[0]
		self.next_piece.remove(self.curr_piece)
		self.next_piece.append(random.choice([L_1(), L_2(), I(), N(), T(), S_1(), S_2()]))

	def clear(self):
		cleared = 0
		for row in range(len(self.pieces)):
			if 0 not in self.pieces[row]:
				cleared = row
				break 

		cleared_pieces = self.pieces[0:cleared]
		self.pieces[1:cleared + 1] = cleared_pieces

	def hold_piece(self):
		if self.held == None:
			self.held = self.curr_piece
			self.spawn_piece()
		else:
			temp = self.held
			self.held = self.curr_piece
			self.curr_piece = temp 
			self.curr_piece.row = self.held.row
			self.curr_piece.col = self.held.col

	#fix
	def check_game_over(self):
		for col in self.pieces[0]:
			if col != 0:
				return True 
			
	def draw_piece(self):
		self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]

		for row in range(self.rows):
				for col in range(self.cols):
					if row == self.curr_piece.get_pos()[0] and col == self.curr_piece.get_pos()[1]:
						for i in range(len(self.curr_piece.get_rotation())):
							for j in range(len(self.curr_piece.get_rotation()[0])):
								new_row = row + i
								new_col = col + j
								if new_row < len(self.grid) and new_col < len(self.grid[0]):
									if self.curr_piece.get_rotation()[i][j] != 0:
										self.grid[new_row][new_col] = self.curr_piece.get_rotation()[i][j]

		for row in range(self.rows):
			for col in range(self.cols):
				if self.pieces[row][col] != 0: 
					self.grid[row][col] = self.pieces[row][col]


	def draw(self, win):
		buffer = 35
		border_size = (HEIGHT - (2 * buffer) - (self.rows * self.space_size)) // 2

		game_outer = (buffer, buffer, (border_size * 2) + self.cols * self.space_size, (border_size * 2) + self.rows * self.space_size)
		pygame.draw.rect(win, GREY_2, game_outer, border_radius=20)

		game_inner = (buffer + border_size, buffer + border_size, self.cols * self.space_size, self.rows * self.space_size)
		pygame.draw.rect(win, GREY_3, game_inner, border_radius=10)

		for row in range(self.rows):
			for col in range(self.cols):
				start_row = (row * self.space_size) + buffer + border_size
				start_col = (col * self.space_size) + buffer + border_size

				color = self.piece_colors[self.grid[row][col]]
				if color != GREY_3:
					radius = 5
				else:
					radius = 0

				border_thickness = 1

				if row == 0 and col == 0:
					pygame.draw.rect(win, GREY_2, (start_col, start_row, self.space_size, self.space_size), border_thickness)
					if color != GREY_3:
						pygame.draw.rect(win, color, (start_col, start_row, self.space_size, self.space_size), border_radius=radius)
				elif row == 0 and col == self.cols - 1:
					pygame.draw.rect(win, GREY_2, (start_col, start_row, self.space_size, self.space_size), border_thickness)
					if color != GREY_3:
						pygame.draw.rect(win, color, (start_col, start_row, self.space_size, self.space_size), border_radius=radius)
				elif row == self.rows - 1 and col == 0:
					pygame.draw.rect(win, GREY_2, (start_col, start_row, self.space_size, self.space_size), border_thickness)
					if color != GREY_3:
						pygame.draw.rect(win, color, (start_col, start_row, self.space_size, self.space_size), border_radius=radius)
				elif row == self.rows - 1 and col == self.cols - 1:
					pygame.draw.rect(win, GREY_2, (start_col, start_row, self.space_size, self.space_size), border_thickness)
					if color != GREY_3:
						pygame.draw.rect(win, color, (start_col, start_row, self.space_size, self.space_size), border_radius=radius)
				else:
					pygame.draw.rect(win, GREY_2, (start_col, start_row, self.space_size, self.space_size), border_thickness)
					if color != GREY_3:
						pygame.draw.rect(win, color, (start_col, start_row, self.space_size, self.space_size), border_radius=radius)

		box_start = 400
		box_width = WIDTH - box_start - buffer - (2 * border_size)
		box_height = 2 * (WIDTH - box_start - buffer) - (2 * border_size)
		num_cells = 4.5
		cell_size = box_width / num_cells
		upper_buffer = (box_height - (cell_size * sum([len(piece.get_rotation()) for piece in self.next_piece]))) // 4

		next_piece_outer = (box_start, buffer, box_width + (2 * border_size), box_height + (2 * border_size))
		pygame.draw.rect(win, GREY_2, next_piece_outer, border_radius=20)

		next_piece_inner = (box_start + border_size, buffer + border_size, box_width, box_height)
		pygame.draw.rect(win, GREY_3, next_piece_inner, border_radius=10)

		start_y = upper_buffer + border_size + buffer
		for piece in self.next_piece:
			start_x = box_start + border_size + (cell_size * (num_cells - len(piece.get_rotation()[0]))) // 2
			for row in range(len(piece.get_rotation())):
				for col in range(len(piece.get_rotation()[0])):
					x = start_x + (col * cell_size)
					y = start_y + (row * cell_size)
					color = self.piece_colors[piece.get_rotation()[row][col]]
					pygame.draw.rect(win, color, (x, y, cell_size, cell_size), border_radius=5)
			start_y += (len(piece.get_rotation()) * cell_size) + upper_buffer

		held_outer = (box_start, (2.5 * buffer) + box_height, box_width + (2 * border_size), (box_height // 3) + (2 * border_size))
		pygame.draw.rect(win, GREY_2, held_outer, border_radius=20)

		held_inner = (box_start + border_size, (2.5 * buffer) + border_size + box_height, box_width, (box_height // 3))
		pygame.draw.rect(win, GREY_3, held_inner, border_radius=10)

		if self.held != None:
			upper_buffer = ((box_height // 3) - (cell_size * len(self.held.rotation_lst[0]))) // 2
			start_y = (2.5 * buffer) + border_size + box_height + upper_buffer 
			start_x = box_start + border_size + (cell_size * (num_cells - len(self.held.rotation_lst[0][0]))) // 2
			for row in range(len(self.held.rotation_lst[0])):
				for col in range(len(self.held.rotation_lst[0][0])):
					x = start_x + (col * cell_size)
					y = start_y + (row * cell_size)
					color = self.piece_colors[self.held.rotation_lst[0][row][col]]
					pygame.draw.rect(win, color, (x, y, cell_size, cell_size), border_radius=5)
			start_y += (len(self.held.rotation_lst[0]) * cell_size) + upper_buffer


class Piece:
	def get_pos(self):
		return self.row, self.col

	def get_rotation(self):
		return self.curr_rotation

	#fix: update to make sure pieces dont go into others when they rotate 
	def can_rotate(self, grid):
		if self.curr_rotation_index < 3:
			index = self.curr_rotation_index + 1

			new_row = self.row - self.offset_list[index - 1][0] + self.offset_list[index][0]
			new_col = self.col - self.offset_list[index - 1][1] + self.offset_list[index][1]

			height = len(self.rotation_lst[index])
			width = len(self.rotation_lst[index][0])
		else: 
			index = 0
			new_row = self.row - self.offset_list[3][0] + self.offset_list[index][0]
			new_col = self.col - self.offset_list[3][1] + self.offset_list[index][1]

			height = len(self.rotation_lst[index])
			width = len(self.rotation_lst[index][0])
			

		if new_row >= 0 and new_row + height - 1 < len(grid) and new_col >= 0 and new_col + width - 1 < len(grid[0]):
			return True
		else:
			return False

	def rotate(self, grid):
		if self.can_rotate(grid):
			if self.curr_rotation_index < 3:
				self.curr_rotation_index += 1
				self.curr_rotation = self.rotation_lst[self.curr_rotation_index]
			else:
				self.curr_rotation_index = 0
				self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

			self.row -= self.offset_list[self.curr_rotation_index - 1][0]
			self.col -= self.offset_list[self.curr_rotation_index - 1][1]

			self.row += self.offset_list[self.curr_rotation_index][0]
			self.col += self.offset_list[self.curr_rotation_index][1]

	def check_pos(self, grid, pos):
		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0])

		if pos[0] >= 0 and pos[0] + self.height - 1 < len(grid) and pos[1] >= 0 and pos[1] + self.width - 1 < len(grid[0]):
			return True
		else:
			return False

	def can_move(self, grid, direction):
		if direction == "left":
			if self.check_pos(grid, [self.row, self.col - 1]): 
				for row in range(len(self.curr_rotation)):
					if self.col > 0:
						if grid[row + self.row][self.col - 1] != 0 and self.curr_rotation[row][0] != 0:
							return False
						else:
							for i in range(self.width):
								if self.curr_rotation[row][i - 1] == 0:
									if grid[row + self.row][self.col + i - 1] != 0 and self.curr_rotation[row][i] != 0:
										return False
			else:
				return False
		if direction == "right":
			if self.check_pos(grid, [self.row, self.col + 1]):
				for row in range(len(self.curr_rotation)):
					if self.col + self.width < len(grid[0]):
						if grid[row + self.row][self.col + self.width] != 0 and self.curr_rotation[row][self.width - 1] != 0:
							return False
						else:
							for i in range(self.width - 1):
								if self.curr_rotation[row][i + 1] == 0:
									if grid[row + self.row][self.col + i + 1] != 0 and self.curr_rotation[row][i] != 0:
										return False
			else:
				return False
		if direction == "down":
			if self.check_pos(grid, [self.row + 1, self.col]):
				for col in range(len(self.curr_rotation[0])):
					if self.row + self.height < len(grid):
						if grid[self.row + self.height][col + self.col] != 0 and self.curr_rotation[self.height - 1][col] != 0:
							return False
						else:
							for i in range(self.height - 1):
								if self.curr_rotation[i + 1][col] == 0:
									if grid[self.row + i + 1][col + self.col] != 0 and self.curr_rotation[i][col] != 0:
										return False
			else:
				return False

		return True

	def move(self, grid, direction):
		if direction == "left":
			if self.can_move(grid, "left"):
				self.col -= 1
		if direction == "right":
			if self.can_move(grid, "right"):
				self.col += 1
		if direction == "down":
			if self.can_move(grid, "down"):
				self.row += 1

class L_1(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3
		self.code = 1

		pos_1 = [[1, 1, 1],
				 [1, 0, 0]]

		pos_1_offset = [1, 0]

		pos_2 = [[1, 1],
				 [0, 1],
				 [0, 1]]

		pos_2_offset = [0, 0]

		pos_3 = [[0, 0, 1],
				 [1, 1, 1]]

		pos_3_offset = [0, 0]

		pos_4 = [[1, 0],
				 [1, 0],
				 [1, 1]]

		pos_4_offset = [0, 1]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

class L_2(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3
		self.code = 2

		pos_1 = [[2, 2, 2],
				 [0, 0, 2]]

		pos_1_offset = [1, 0]

		pos_2 = [[0, 2],
				 [0, 2],
				 [2, 2]]

		pos_2_offset = [0, 0]

		pos_3 = [[2, 0, 0],
				 [2, 2, 2]]

		pos_3_offset = [0, 0]

		pos_4 = [[2, 2],
				 [2, 0],
				 [2, 0]]

		pos_4_offset = [0, 1]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

class I(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3
		self.code = 3

		pos_1 = [[3, 3, 3, 3]]

		pos_1_offset = [1, 0]

		pos_2 = [[3],
				 [3],
				 [3],
				 [3]]

		pos_2_offset = [0, 2]

		pos_3 = [[3, 3, 3, 3]]

		pos_3_offset = [2, 0]

		pos_4 = [[3],
				 [3],
				 [3],
				 [3]]

		pos_4_offset = [0, 1]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

class N(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3 
		self.code = 4

		pos_1 = [[4, 4],
				 [4, 4]]

		pos_1_offset = [1, 0]

		pos_2 = [[4, 4],
				 [4, 4]]

		pos_2_offset = [1, 0]

		pos_3 = [[4, 4],
				 [4, 4]]

		pos_3_offset = [1, 0]

		pos_4 = [[4, 4],
				 [4, 4]]

		pos_4_offset = [1, 0]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

class T(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3
		self.code = 5

		pos_1 = [[0, 5, 0],
				 [5, 5, 5]]

		pos_1_offset = [0, 0]

		pos_2 = [[5, 0],
				 [5, 5],
				 [5, 0]]

		pos_2_offset = [0, 1]

		pos_3 = [[5, 5, 5],
				 [0, 5, 0]]

		pos_3_offset = [1, 0]

		pos_4 = [[0, 5],
				 [5, 5],
				 [0, 5]]

		pos_4_offset = [0, 0]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

class S_1(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3
		self.code = 6

		pos_1 = [[0, 6, 6],
				 [6, 6, 0]]

		pos_1_offset = [0, 0]

		pos_2 = [[6, 0],
				 [6, 6],
				 [0, 6]]

		pos_2_offset = [0, 1]

		pos_3 = [[0, 6, 6],
				 [6, 6, 0]]

		pos_3_offset = [1, 0]

		pos_4 = [[6, 0],
				 [6, 6],
				 [0, 6]]

		pos_4_offset = [0, 0]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

class S_2(Piece):
	def __init__(self):
		self.row = -1
		self.col = 3
		self.code = 7

		pos_1 = [[7, 7, 0],
				 [0, 7, 7]]

		pos_1_offset = [0, 0]

		pos_2 = [[0, 7],
				 [7, 7],
				 [7, 0]]

		pos_2_offset = [0, 1]

		pos_3 = [[7, 7, 0],
				 [0, 7, 7]]

		pos_3_offset = [1, 0]

		pos_4 = [[0, 7],
				 [7, 7],
				 [7, 0]]

		pos_4_offset = [0, 0]

		self.rotation_lst = [pos_1, pos_2, pos_3, pos_4]
		self.offset_list = [pos_1_offset, pos_2_offset, pos_3_offset, pos_4_offset]
		self.curr_rotation_index = 0
		self.curr_rotation = self.rotation_lst[self.curr_rotation_index]

		self.height = len(self.curr_rotation)
		self.width = len(self.curr_rotation[0]) 

def update(win, grid):
	win.fill(GREY_1)
	grid.draw(win)

	grid.draw_piece()

	pygame.display.update()

def main():
	grid = Grid()

	last_time = time.time()

	run = True
	while run:
		
		if time.time() - last_time > grid.time_between:
			grid.update_pieces()
			last_time = time.time()

		grid.clear()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False 
				break

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					grid.get_current_piece().rotate(grid.get_grid())

				elif event.key == pygame.K_DOWN:
					grid.get_current_piece().move(grid.get_grid(), "down")
				elif event.key == pygame.K_LEFT:
					grid.get_current_piece().move(grid.get_grid(), "left")
				elif event.key == pygame.K_RIGHT:
					grid.get_current_piece().move(grid.get_grid(), "right")

				elif event.key == pygame.K_SPACE:
					while grid.get_current_piece().can_move(grid.get_grid(), "down"):
						grid.get_current_piece().move(grid.get_grid(), "down")

				elif event.key == pygame.K_h:
					grid.hold_piece()

		if grid.check_game_over(): 
			run = False   

		update(WINDOW, grid)

	pygame.quit()

if __name__ == "__main__":
	main()