import pygame
from pygame.locals import *
import random

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

colors = [BLACK, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]

# This class represents the Tetrominoes
class Tetromino:
    # Constructor. Pass in the color of the block and its x and y position
    def __init__(self):
        self.color = random.choice(colors[1:])
        self.shape = random.choice(list(shapes.values()))
        self.rotation = 0
        self.x = int(grid_width / 2) - int(tetromino_size / 2)
        self.y = 0

    # Call this function to rotate the Tetromino
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

    # Call this function to draw the Tetromino on the screen
    def draw(self):
        for y in range(tetromino_size):
            for x in range(tetromino_size):
                if self.shape[self.rotation][y][x]:
                    pygame.draw.rect(screen, self.color,
                                     [margin + (self.x + x) * block_size + grid_line_width,
                                      margin + (self.y + y) * block_size + grid_line_width,
                                      block_size - grid_line_width * 2,
                                      block_size - grid_line_width * 2])

    # Call this function to check if the Tetromino is colliding with the walls or other blocks
    def is_colliding(self, dx=0, dy=0):
        for y in range(tetromino_size):
            for x in range(tetromino_size):
                if self.shape[self.rotation][y][x]:
                    new_x = self.x + dx + x
                    new_y = self.y + dy + y
                    if new_x < 0 or new_x >= grid_width or new_y < 0 or new_y >= grid_height or grid[new_y][new_x]:
                        return True
        return False

# This class represents the grid of blocks
class Grid:
    # Constructor. Pass in the color of the block and its x and y position
    def __init__(self):
        self.grid = [[None for _ in range(grid_width)] for _ in range(grid_height)]

    # Call this function to draw the blocks on the screen
    def draw(self):
        for y in range(grid_height):
            for x in range(grid_width):
                color = self.grid[y][x]
                if color:
                    pygame.draw.rect(screen, color,
                                     [margin + x * block_size + grid_line_width,
                                      margin + y * block_size + grid_line_width,
                                      block_size - grid_line_width * 2,
                                      block_size - grid_line_width * 2])

    # Call this function to add a Tetromino to the grid
    def add_tetromino(self, tetromino):
        for y in range(tetromino_size):
            for x in range(tetromino_size):
                if tetromino.shape[tetromino.rotation][y][x]:
                    self.grid[tetromino.y + y][tetromino.x + x] = tetromino.color

    # Call this function to check and remove full rows from the grid
    def check_rows(self):
        rows_to_remove = []
        for y in range(grid_height):
            if all(self.grid[y]):
                rows_to_remove.append(y)
        for row in rows_to_remove:
            del self.grid[row]
            self.grid.insert(0, [None for _ in range(grid_width)])
        return len(rows_to_remove)

# Set up some global variables
grid_width = 10
grid_height = 20
block_size = 30
grid_line_width = 2
margin = block_size * 2

tetromino_size = 4

shapes = {
    'I': [
        [
            [False] * tetromino_size,
            [True] * tetromino_size,
            [False] * tetromino_size,
            [False] * tetromino_size,
        ],
        [
            [False] * tetromino_size,
            [False] * tetromino_size,
            [False] * tetromino_size,
            [True] * tetromino_size,
        ],
        [
            [False] * tetromino_size,
            [False] * tetromino_size,
            [True] * tetromino_size,
            [False] * tetromino_size,
        ],
        [
            [True] * tetromino_size,
            [False] * tetromino_size,
            [False] * tetromino_size,
            [False] * tetromino_size,
        ],
    ],
    'J': [
        [
            [True, False, False],
            [True, True, True],
            [False, False, False],
        ],
        [
            [False, True, True],
            [False, True, False],
            [False, True, False],
        ],
        [
            [False, False, False],
            [True, True, True],
            [False, False, True],
        ],
        [
            [False, True, False],
            [False, True, False],
            [True, True, False],
        ],
    ],
    'L': [
        [
            [False, False, True],
            [True, True, True],
            [False, False, False],
        ],
        [
            [False, True, False],
            [False, True, False],
            [False, True, True],
        ],
        [
            [False, False, False],
            [True, True, True],
            [True, False, False],
        ],
        [
            [True, True, False],
            [False, True,False],
            [False,True,False]
        ]
    ],
    'O': [
        [
            [True,True],
            [True,True]
        ]
    ]*4,
    'S': [
        [
           [False,True,True],
           [True,True,False],
           [False,False,False]
       ],
       [
           [True,False,False],
           [True,True,False],
           [False,True,False]
       ],
       [
           [False,False,False],
           [False,True,True],
           [True,True,False]
       ],
       [
           [True,True,False],
           [False,True,True],
           [False,False,False]
       ]
    ],
    'T':[
       [
           [True,True,True],
           [False,True,False],
           [False,False,False]
       ],
       [
           [True,False,False],
           [True,True,False],
           [True,False,False]
       ],
       [
           [False,False,False],
           [True,True,True],
           [False,True,False]
       ],
       [
           [False,True,False],
           [True,True,False],
          [False,True,False]
       ]
   ],
   'Z':[
       [
         	[True,True,False],
         	[False,True,True],
         	[False,False,False]
         ],
         [[0]*tetromino_size]*4
   ]
}

# Set the width and height of the screen
size = (grid_width * block_size + margin * 2 + grid_line_width * grid_width,
        grid_height * block_size + margin * 2 + grid_line_width * grid_height)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

grid = Grid()
current_tetromino = Tetromino()
next_tetromino = Tetromino()

score = 0
level = 1
speed = 48

frame_count = 0

font = pygame.font.Font(None, 36)

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if not current_tetromino.is_colliding(dx=-1):
                    current_tetromino.x -= 1
            elif event.key == K_RIGHT:
                if not current_tetromino.is_colliding(dx=1):
                    current_tetromino.x += 1
            elif event.key == K_DOWN:
                if not current_tetromino.is_colliding(dy=1):
                    current_tetromino.y += 1
                else:
                    grid.add_tetromino(current_tetromino)
                    score += grid.check_rows() * 10
                    level = score // 100 + 1
                    speed = max(48 - level * 5 + level // 5 * 2 + level // 10 * 3 + level // 15 * 5 + level // 20 * 10,
                                1)
                    current_tetromino = next_tetromino
                    next_tetromino = Tetromino()
                    if current_tetromino.is_colliding():
                        done