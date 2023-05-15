from blocks import *
import random, pygame
from assets import *
import sys

class Colors:
	dark_grey = (26, 31, 40)
	green = (47, 230, 23)
	red = (232, 18, 18)
	orange = (226, 116, 17)
	yellow = (237, 234, 4)
	purple = (166, 0, 247)
	cyan = (21, 204, 209)
	blue = (13, 64, 216)
	white = (255, 255, 255)
	dark_blue = (44, 44, 127)
	light_blue = (59, 85, 162)

	@classmethod
	def get_cell_colors(cls):
		return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]

class Grid:
	def __init__(self):
		self.num_rows = 20
		self.num_cols = 10
		self.cell_size = 30
		self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
		self.colors = Colors.get_cell_colors()

	def print_grid(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				print(self.grid[row][column], end = " ")
			print()

	def is_inside(self, row, column):
		if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
			return True
		return False

	def is_empty(self, row, column):
		if self.grid[row][column] == 0:
			return True
		return False

	def is_row_full(self, row):
		for column in range(self.num_cols):
			if self.grid[row][column] == 0:
				return False
		return True

	def clear_row(self, row):
		for column in range(self.num_cols):
			self.grid[row][column] = 0

	def move_row_down(self, row, num_rows):
		for column in range(self.num_cols):
			self.grid[row+num_rows][column] = self.grid[row][column]
			self.grid[row][column] = 0

	def clear_full_rows(self):
		completed = 0
		for row in range(self.num_rows-1, 0, -1):
			if self.is_row_full(row):
				self.clear_row(row)
				completed += 1
			elif completed > 0:
				self.move_row_down(row, completed)
		return completed

	def reset(self):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				self.grid[row][column] = 0

	def draw(self, screen):
		for row in range(self.num_rows):
			for column in range(self.num_cols):
				cell_value = self.grid[row][column]
				cell_rect = pygame.Rect(column*self.cell_size + 11, row*self.cell_size + 11,
				self.cell_size -1, self.cell_size -1)
				pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

class Button:
    def __init__(self, x, y, width, height, color, hover_color, text, text_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont('FiraSans-Bold.ttf', 76)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.hover_color if self.is_hovered else self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

class Game:
	@staticmethod
	def get_record():
		try:
			with open('record.txt') as f:
				return int(f.readline())
		except FileNotFoundError:
			with open('record.txt', 'w') as f:
				f.write('0')
				return 0
	@staticmethod
	def set_record(record, score):
		rec = max(record, score)
		with open('record.txt', 'w') as f:
			f.write(str(rec))
	
	def __init__(self):
		self.grid = Grid()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.game_over = False
		self.score = 0
		self.rotate_sound = pygame.mixer.Sound('effects/rotate.wav')
		self.clear_sound = pygame.mixer.Sound('effects/lineclear.wav')
		self.game_over_sound = pygame.mixer.Sound('effects/gameover.wav')
		self.block_drop_sound = pygame.mixer.Sound('effects/drop.wav')
		self.state = "MENU"  # Initial state is MENU
		
		pygame.mixer.music.load('songs/savanasong.wav')
		pygame.mixer.music.play(-1)
		
		self.buttons = []
		self.level_buttons = []
		self.selected_button = None

		self.create_buttons(["Start", "Records", "Quit"], self.buttons)
	
	def create_buttons(self, name_of_the_buttons, list_of_buttons):
		num_rows = 20
		num_cols = 10
		for i, button_name in enumerate(name_of_the_buttons):
			button = Button(
				500 / 2,
				840 / 2 + i * (num_cols * 3),
				num_rows * 5,
				num_cols * 4,
				'#000000',
				'#E74343',
				button_name,
				'#FFFFFF',
				self.handle_button_events 
			)
			list_of_buttons.append(button)
	
	def handle_button_events(self, event):
		if self.state == "MENU":
			for button in self.buttons:
				if button.rect.collidepoint(event.pos):
					self.selected_button = button
				if button.text == "Start":
					self.state = "LEVEL_MENU"
				elif button.text == "Records":
					self.show_stats()
				else:
					pygame.quit()
					sys.exit()
		elif self.state == "LEVEL_MENU":
			for button in self.level_buttons:
				if button.rect.collidepoint(event.pos):
					self.selected_button = button
					self.start_game_with_level()
		
	def show_stats(self):
		record = self.get_record()
		while True:
			with open("record.txt", "r") as file:
				file_contents = file.read()
			lines = file_contents.split("\n")
			max_score = max([int(line) for line in lines if line.strip()])  # Filter out empty lines
			while True:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							pygame.quit()
							sys.exit()
				screen.fill((255, 255, 255))
				screen.blit
		
	def update_score(self, lines_cleared, move_down_points):
		if lines_cleared == 1:
			self.score += 100
		elif lines_cleared == 2:
			self.score += 300
		elif lines_cleared == 3:
			self.score += 500
		self.score += move_down_points
		
		record = self.get_record()
		if self.score > record:
			self.set_record(record, self.score)
		
		record = self.get_record()

	def get_random_block(self):
		if len(self.blocks) == 0:
			self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		block = random.choice(self.blocks)
		self.blocks.remove(block)
		return block

	def move_left(self):
		self.current_block.move(0, -1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, 1)

	def move_right(self):
		self.current_block.move(0, 1)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(0, -1)

	def move_down(self):
		self.current_block.move(1, 0)
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.move(-1, 0)
			self.lock_block()

	def lock_block(self):
		tiles = self.current_block.get_cell_positions()
		for position in tiles:
			self.grid.grid[position.row][position.column] = self.current_block.id
		self.current_block = self.next_block
		self.next_block = self.get_random_block()
		rows_cleared = self.grid.clear_full_rows()
		if rows_cleared > 0:
			self.clear_sound.play()
			self.update_score(rows_cleared, 0)
		if self.block_fits() == False:
			self.game_over = True

	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0

	def block_fits(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_empty(tile.row, tile.column) == False:
				return False
		return True

	def rotate(self):
		self.current_block.rotate()
		if self.block_inside() == False or self.block_fits() == False:
			self.current_block.undo_rotation()
		else:
			self.rotate_sound.play()

	def block_inside(self):
		tiles = self.current_block.get_cell_positions()
		for tile in tiles:
			if self.grid.is_inside(tile.row, tile.column) == False:
				return False
		return True
	
	def reset(self):
		self.grid.reset()
		self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
		self.current_block = self.get_random_block()
		self.next_block = self.get_random_block()
		self.score = 0
		self.game_over = False

	def draw(self, screen):
		self.grid.draw(screen)
		self.current_block.draw(screen, 11, 11)

		if self.next_block.id == 3:
			self.next_block.draw(screen, 255, 290)
		elif self.next_block.id == 4:
			self.next_block.draw(screen, 255, 280)
		else:
			self.next_block.draw(screen, 270, 270)
	
	def start_game_with_level(self, level):
		pass