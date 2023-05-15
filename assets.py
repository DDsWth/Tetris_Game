import pygame

pygame.init()

screen_width, screen_height = 500, 840
screen = pygame.display.set_mode((screen_width, screen_height))

backgrounds = [
    pygame.image.load('backgrounds\savanabg.jpg'),
    pygame.image.load('backgrounds\stalkerbg.jpg'),
    pygame.image.load('backgrounds\spacebg.jpg'),
    pygame.image.load('backgrounds\logo.png')
]

fontStyle = [
    pygame.font.Font('Fonts\FiraSans-Bold.ttf', 45), #Title font
    pygame.font.Font('Fonts\FiraMono-Medium.ttf', 20) #Description font
]
