from functions import *

buttons, level_buttons = [], []
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

def create_buttons(name_of_the_buttons, list_of_buttons):
    for i, button_name in enumerate(name_of_the_buttons):
        print(i, button_name)
        button = Button(
            int(screen_width / 2),
            int(screen_height / 2) + i * (tile_height * 3),
            tile_width * 5,
            tile_height * 4,
            '#000000',
            '#E74343',
            button_name,
            '#FFFFFF'
        )
        list_of_buttons.append(button)

create_buttons(["Start", "Records", "Quit"], buttons)
create_buttons(['First lvl', 'Second lvl', 'Third lvl'], level_buttons)

def handle_button_events(event):
    global selected_button
    for i, button in enumerate(buttons):
        if button.rect.collidepoint(event.pos):
            selected_button = button
            if button.text == "Start":
                choose_level_menu()
            if button.text == "Records":
                show_stats()
            else:
                quitGame()

    for i, button in enumerate(level_buttons):
        if button.rect.collidepoint(event.pos):
            selected_button = button

def choose_level_menu():
    global selected_button
    rectangle_color = '#000000'
    rectangle_position = (250, 485)
    rectangle_size = (400, 200)
    pygame.draw.rect(window, rectangle_color, (rectangle_position, rectangle_size))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in level_buttons:
                    if button.rect.collidepoint(event.pos):
                        selected_button = button
                        window.fill('#000000')
                        pygame.display.flip()
                        if button.text == "First lvl":
                            play_sound(sounds[0])
                            play_tetris(0)
                            pass
                        elif button.text == "Second lvl":
                            play_sound(sounds[1])
                            play_tetris(2)
                            pass
                        elif button.text == "Third lvl":
                            play_sound(sounds[2])
                            play_tetris(4)
                            pass

        for button in level_buttons:
            button.draw()  # Remove the "window" argument

        pygame.display.flip()

def check_borders():
    for i in range(4):
        if figure[i].x < 0 or figure[i].x > tile_width - 1:
            return False
        elif figure[i].y > tile_height - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True

def play_tetris(bg_number):
    global field  # Declare paused as a global variable
    score, lines = 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
    anim_count, anim_speed, anim_limit = 0, 60, 2000
    field = [[0 for i in range(tile_width)] for j in range(tile_height)]
    clock = pygame.time.Clock()
    figure_rect = pygame.Rect(0, 0, tile_size - 2, tile_size - 2)
    get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = get_color(), get_color()

    while True:
        record = get_record()
        dx, rotate = 0, False
        window.blit(backgrounds[int(bg_number)], (0, 0))
        window.blit(game_area, (20, 20))
        game_area.blit(backgrounds[int(bg_number+1)], (0, 0))
        for i in range(lines):
            pygame.time.wait(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    anim_limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True
        
        # X movement
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
            
        # Y movement
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
                
        # Rotation of the block
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
                
        # Whether the line is full condition
        line, lines = tile_height - 1, 0
        for row in range(tile_height - 1, -1, -1):
            count = 0
            for i in range(tile_width):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < tile_width:
                line -= 1
            else:
                anim_speed += 3
                lines += 1
        
        score += scores[lines]  # Score computing
        
        [pygame.draw.rect(game_area, (40, 40, 40), i_rect, 1) for i_rect in grid] # Grid drawing
        
        # Figure drawing
        for i in range(4):
            figure_rect.x = figure[i].x * tile_size
            figure_rect.y = figure[i].y * tile_size
            pygame.draw.rect(game_area, color, figure_rect)
        
        # Field drawing
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * tile_size, y * tile_size
                    pygame.draw.rect(game_area, col, figure_rect)
       
        # Next block drawing
        for i in range(4):
            figure_rect.x = next_figure[i].x * tile_size + 380
            figure_rect.y = next_figure[i].y * tile_size + 185
            pygame.draw.rect(window, next_color, figure_rect)
        
        # Game UI
        window.blit(fontStyle[0].render('Next Block', True, pygame.Color('darkorange')), (495, 50))
        window.blit(fontStyle[1].render('Your record:', True, pygame.Color('#FFFFFF')), (550, 320))
        window.blit(fontStyle[0].render(record, True, pygame.Color('gold')), (595, 360))
        window.blit(fontStyle[1].render('Scores:', True, pygame.Color('green')), (600, 520))
        window.blit(fontStyle[1].render(str(score), True, pygame.Color('white')), (605, 560))
        window.blit(fontStyle[0].render(record, True, pygame.Color('gold')), (595, 360))
        
        # Game over
        for i in range(tile_width):
            if field[0][i]:
                set_record(record, score)
                field = [[0 for i in range(tile_width)] for i in range(tile_height)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                for i_rect in grid:
                    pygame.draw.rect(game_area, get_color(), i_rect)
                    window.blit(game_area, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
        pygame.display.flip()
        clock.tick(FPS)
            
def main_menu():
    global selected_button
    start_button_pressed = False
    
    while not start_button_pressed:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_button_events(event)

        for i, button in enumerate(buttons):
            button.draw()
        pygame.display.update()

        if selected_button is not None:
            if selected_button.text == "Start":
                start_button_pressed = True

def show_stats():
    with open("record.txt", "r") as file:
        file_contents = file.read()
    lines = file_contents.split("\n")
    max_score = max([int(line) for line in lines if line.strip()])  # Filter out empty lines
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitGame()
        window.fill((255, 255, 255))
        window.blit(fontStyle[0].render(f'Your best score: {max_score}', True, pygame.Color('#FF9E00')), (215, -10))
        window.blit(fontStyle[1].render(f'Press ESCAPE to close the game', True, pygame.Color('#94F500')), (235, 40))
        pygame.display.flip()

def main():
    window.blit(background_img, (0, 0))
    main_menu()
    pygame.display.update()
    choose_level_menu()

main()