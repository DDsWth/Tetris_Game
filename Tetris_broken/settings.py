import pygame
from copy import deepcopy
from random import choice, randrange

pygame.init()

TETROMINOES = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

sounds = [
    'effects\savanasong.wav', 
    'effects\spacesong.wav',
    'effects\pollutionsong.wav',
    'effects\drop.wav', 
    'effects\gameoverwav',
    'effects\lineclear.wav'
]

backgrounds = [
    pygame.image.load('backgrounds\savanabg.jpg'),
    pygame.image.load('backgrounds\savanascreen.jpg'),
    pygame.image.load('backgrounds\stalkerbg.jpg'),
    pygame.image.load('backgrounds\stalkerscreen.jpg'),
    pygame.image.load('backgrounds\spacebg.jpg'),
    pygame.image.load('backgrounds\spacescreen.jpg'),
    pygame.image.load('backgrounds\logo.png')
]

fontStyle = [
    pygame.font.Font('Fonts\FiraSans-Bold.ttf', 45), #Title font
    pygame.font.Font('Fonts\FiraMono-Medium.ttf', 20) #Description font
]

tile_width, tile_height = 10, 20
tile_size = 45
game_resolution = tile_width * tile_size, tile_height * tile_size
screen_width, screen_height = 750, 940
grid = [pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size) for x in range(tile_width) for y in range(tile_height)]
window = pygame.display.set_mode((screen_width, screen_height))
game_area = pygame.Surface(game_resolution)
background_img = pygame.transform.scale(backgrounds[6], (screen_width, screen_height //2))
another_example_img = pygame.transform.scale(backgrounds[5], (screen_width, screen_height //2))
FPS = 60

figures = [[pygame.Rect(x + tile_width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in TETROMINOES]