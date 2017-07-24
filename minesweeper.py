from tkinter import *
import random

class Minesweeper(object):
	def __init__(self, lvl=0):
		self.lvl = lvl
		
		if self.lvl == 1:
			self.num_rows = 16
			self.num_cols = 16
			self.num_mines = 40
		elif self.lvl == 2:
			self.num_rows = 16
			self.num_cols = 30
			self.num_mines = 99
		else:
			self.num_rows = 9
			self.num_cols = 9
			self.num_mines = 10

		self.cell_size = 20
		self.margin = 10
		self.mine_width = self.cell_size * self.num_cols
		self.mine_height = self.cell_size * self.num_rows
		self.menu_height = 50
		self.menu_width = self.mine_width

		self.width = self.margin * 4 + self.mine_width
		self.height = self.margin * 5 + self.mine_height + self.menu_height

		self.x = self.margin * 2
		self.y = self.margin * 3 + self.menu_height
		self.curr_col = -1
		self.curr_row = -1
		self.happy_face = ':)'
		self.sad_face = ':('
		self.win_face = 'xD'
		self.face = self.happy_face
		self.is_game_over = False

		self.root = Tk()
		self.canvas = Canvas(self.root, width=self.width, height=self.height)
		self.canvas.pack()
		self.root.bind('<Button-1>', self.btn1)
		self.root.bind('<Button-2>', self.btn2)
		self.root.bind('<Motion>', self.motion)
		self.root.bind('<Key>', self.key)

		self.delay = 10
		self.mine_count = self.num_mines
		self.flag_count = 0
		self.time = 0

		self.generate_board()
		self.board_status = [[False] * self.num_cols
			for _ in range(self.num_rows)]

	def check_win(self):
		if self.is_game_over == True: return
		self.is_game_over = True
		for row_ind in range(self.num_rows):
			for col_ind in range(self.num_cols):
				if (self.board[row_ind][col_ind] == -1 and
					self.board_status[row_ind][col_ind] != '!'):
					self.is_game_over = False
		if self.is_game_over:
			self.face = self.win_face

	def show_neighbours(self, prev_row_ind, prev_col_ind,
		prev_dr, prev_dc, s=None):
		if s == None:
			s = set()
		row_ind = prev_row_ind + prev_dr
		col_ind = prev_col_ind + prev_dc
		if (row_ind, col_ind) in s:
			return
		s.add((row_ind, col_ind))
		if self.board[row_ind][col_ind] != 0:
			self.board_status[row_ind][col_ind] = True
		else:
			self.board_status[row_ind][col_ind] = True
			for (dr, dc) in (          (-1, -0),
							 (-0, -1),           (+0, +1),
				                       (+1, +0)):
				nrow, ncol = row_ind + dr, col_ind + dc
				if (nrow not in range(self.num_rows) or
					ncol not in range(self.num_cols)):
					continue
				if dr == -prev_dr and dc == -prev_dc:
					continue
				self.show_neighbours(row_ind, col_ind, dr, dc, s)

	def show_zeros(self, row_ind, col_ind):
		if self.board[row_ind][col_ind] != -1:
			self.board_status[row_ind][col_ind] = True
		for (dr, dc) in (          (-1, -0),
						 (-0, -1),           (+0, +1),
			                       (+1, +0)):
			nrow, ncol = row_ind + dr, col_ind + dc
			if (nrow not in range(self.num_rows) or
				ncol not in range(self.num_cols)):
				continue
			if self.board[nrow][ncol] == 0:
				self.show_neighbours(row_ind, col_ind, dr, dc)

	def btn1(self, event):
		if (self.width / 2 - self.cell_size / 2 <= event.x <=
			self.width / 2 + self.cell_size / 2 and
			self.margin * 2 + (self.menu_height - self.cell_size) / 2 <= event.y
			<= self.margin * 2 + (self.menu_height + self.cell_size) / 2):
			self.generate_board()
			self.board_status = [[False] * self.num_cols
				for _ in range(self.num_rows)]
			self.time = 0
			self.mine_count = self.num_mines
			self.face = self.happy_face
			self.flag_count = 0
			self.is_game_over = False
			return
		if (event.x < self.x or event.x > self.x + self.mine_width or
			event.y < self.y or event.y > self.y + self.mine_height):
			return
		col = (event.x - self.x) // self.cell_size
		row = (event.y - self.y) // self.cell_size
		if self.board_status[row][col] == False:
			self.show_zeros(row, col)
		if self.board[row][col] == -1:
			self.board_status[row][col] = True
			self.face = self.sad_face
			self.is_game_over = True
		self.check_win()

	def num_flags(self, row_ind, col_ind):
		count = 0
		for drow, dcol in ((-1, -1), (-1, -0), (-1, +1),
						   (-0, -1),           (+0, +1),
						   (+1, -1), (+1, +0), (+1, +1)):
			r, c = row_ind + drow, col_ind + dcol
			if r not in range(self.num_rows) or c not in range(self.num_cols):
				continue
			if self.board_status[r][c] == '!':
				count += 1
		return count

	def has_misplaced_flag(self, row_ind, col_ind):
		for drow, dcol in ((-1, -1), (-1, -0), (-1, +1),
						   (-0, -1),           (+0, +1),
						   (+1, -1), (+1, +0), (+1, +1)):
			r, c = row_ind + drow, col_ind + dcol
			if r not in range(self.num_rows) or c not in range(self.num_cols):
				continue
			if self.board_status[r][c] == '!' and self.board[r][c] != -1:
				return True
		return False

	def show_all_mines(self):
		for row_ind in range(self.num_rows):
			for col_ind in range(self.num_cols):
				if self.board[row_ind][col_ind] == -1:
					self.board_status[row_ind][col_ind] = True

	def show_surrounding(self, row_ind, col_ind):
		for drow, dcol in ((-1, -1), (-1, -0), (-1, +1),
						   (-0, -1),           (+0, +1),
						   (+1, -1), (+1, +0), (+1, +1)):
			r, c = row_ind + drow, col_ind + dcol
			if r not in range(self.num_rows) or c not in range(self.num_cols):
				continue
			self.show_zeros(r, c)

	def btn2(self, event):
		if self.is_game_over: return
		if (event.x < self.x or event.x > self.x + self.mine_width or
			event.y < self.y or event.y > self.y + self.mine_height):
			return
		col = (event.x - self.x) // self.cell_size
		row = (event.y - self.y) // self.cell_size
		if self.board_status[row][col] == False:
			if self.flag_count < self.num_mines:
				self.board_status[row][col] = '!'
				self.mine_count -= 1
				self.flag_count += 1
		elif self.board_status[row][col] == '!':
			self.board_status[row][col] = False
			self.mine_count += 1
			self.flag_count -= 1
		elif self.board_status[row][col] == True:
			if (self.num_flags(row, col) == self.board[row][col] and
				self.board[row][col] != 0):
				if self.has_misplaced_flag(row, col):
					self.face = self.sad_face
					self.is_game_over = True
					self.show_all_mines()
				else:
					self.show_surrounding(row, col)
		self.check_win()

	def motion(self, event):
		if (event.x < self.x or event.x > self.x + self.mine_width or
			event.y < self.y or event.y > self.y + self.mine_height):
			return
		self.curr_col = (event.x - self.x) // self.cell_size
		self.curr_row = (event.y - self.y) // self.cell_size

	def key(self, event):
		if event.keysym == 'k':
			self.board_status = [[True] * self.num_cols
				for _ in range(self.num_rows)]
		elif event.keysym == 'p':
			self.print_board()

	def generate_board(self):
		self.board = [[None] * self.num_cols for _ in range(self.num_rows)]
		mines = [(x, y) for x in range(self.num_cols)
			for y in range(self.num_rows)]
		random.shuffle(mines)
		for _ in range(self.num_mines):
			(x, y) = mines.pop()
			self.board[y][x] = -1
		for row_ind in range(self.num_rows):
			for col_ind in range(self.num_cols):
				if self.board[row_ind][col_ind] == None:
					self.board[row_ind][col_ind] = 0
					for (drow, dcol) in [(-1, -1), (-1, 0), (-1, 1),
										 ( 0, -1),          ( 0, 1),
										 ( 1, -1), ( 1, 0), ( 1, 1)]:
						nrow, ncol = row_ind + drow, col_ind + dcol
						if (nrow in range(self.num_rows) and
							ncol in range(self.num_cols)):
							if self.board[nrow][ncol] == -1:
								self.board[row_ind][col_ind] += 1

	def print_board(self):
		for row in self.board:
			for cell in row:
				print('%3d' % cell, end=' ')
			print()

	def draw_ui(self):
		self.canvas.create_rectangle(self.margin, self.margin,
			self.width - self.margin, self.height - self.margin)
		self.canvas.create_rectangle(self.margin * 2, self.margin * 2,
			self.width - self.margin * 2, self.menu_height + self.margin * 2)
		self.canvas.create_rectangle(
			self.margin * 2,
			self.margin * 3 + self.menu_height,
			self.width - self.margin * 2, 
			self.height - self.margin * 2)

	def draw_mine_count(self):
		self.canvas.create_text(self.margin * 2, self.margin * 2,
			text=str(self.mine_count), anchor=NW)

	def draw_time(self):
		self.canvas.create_text(self.width - self.margin * 2,
			self.margin * 2, text=str(int(self.time)), anchor=NE)

	def draw_face(self):
		self.canvas.create_rectangle(self.width / 2 - self.cell_size / 2,
			self.margin * 2 + self.menu_height / 2 - self.cell_size / 2,
			self.width / 2 + self.cell_size / 2,
			self.margin * 2 + self.menu_height / 2 + self.cell_size / 2)
		self.canvas.create_text(self.width / 2,
			self.margin * 2 + self.menu_height / 2,
			text=self.face, font='Courier')

	def draw_menu(self):
		self.draw_mine_count()
		self.draw_time()
		self.draw_face()

	def draw_board(self):
		for row_ind in range(self.num_rows):
			for col_ind in range(self.num_cols):
				x0 = self.x + col_ind * self.cell_size
				y0 = self.y + row_ind * self.cell_size
				x1 = x0 + self.cell_size
				y1 = y0+ self.cell_size
				xt = x0 + self.cell_size / 2
				yt = y0 + self.cell_size / 2
				t = str(self.board[row_ind][col_ind])
				self.canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
				if self.board_status[row_ind][col_ind] == True:
					self.canvas.create_text(xt, yt, text=t)
				elif self.board_status[row_ind][col_ind] == '!':
					self.canvas.create_text(xt, yt, text='!')

	def draw_highlight(self):
		if (self.curr_row not in range(self.num_rows) or
			self.curr_col not in range(self.num_cols)):
			return
		x0 = self.x + self.curr_col * self.cell_size
		y0 = self.y + self.curr_row * self.cell_size
		x1 = x0 + self.cell_size
		y1 = y0 + self.cell_size
		self.canvas.create_rectangle(x0, y0, x1, y1, outline='yellow')

	def redraw(self):
		self.canvas.delete(ALL)

		self.draw_ui()
		self.draw_menu()
		self.draw_board()
		self.draw_highlight()

		self.canvas.update()

	def timer(self):
		if not self.is_game_over:
			self.time += .05
		self.redraw()
		self.canvas.after(self.delay, self.timer)

	def run(self):
		self.timer()
		self.root.mainloop()

minesweeper = Minesweeper()
minesweeper.run()