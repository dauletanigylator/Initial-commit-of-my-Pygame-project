
import pygame
import sys
import random

pygame.init()

TILE_SIZE = 80
FONT_SIZE = 32

# COLOR CHANGE TO IMAGE
tiles = {
    'empty': (255, 255, 255),  # White
    'wall': (0, 0, 0),         # Black
    'goal': pygame.image.load("goal.png"),
    'door': pygame.image.load("door.png"),
    'key': pygame.image.load("key.png"),
    'coin': pygame.image.load("coin.png"),
    'power_up': pygame.image.load("power_up.png"),
    'won': pygame.image.load("won.png")
}
'''
7 - won
6 - power_up
5 - coin
4 - KEY
3 - door
2 - goal
'''
# LEVELS & DESCRIP
levels = [
    #LEVEL1
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 2, 0, 1],
        [1, 5, 1, 0, 1, 1, 3, 1],
        [1, 0, 1, 5, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 4, 1, 0, 0, 1],
        [1, 5, 1, 0, 5, 0, 5, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ],
    #LEVEL2
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 2, 0, 3, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 4, 0, 0, 0, 0, 5, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    #LEVEL3
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 2, 0, 0, 3, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 5, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 5, 1, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0, 0, 4, 1, 0, 1],
        [1, 0, 0, 0, 5, 1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    #LEVEL4
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 2, 1, 3, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 5, 1],
        [1, 1, 1, 0, 1, 1, 4, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 5, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 5, 1],
        [1, 0, 0, 5, 0, 0, 6, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 5, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ],
    #LEVEL5
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 5, 1, 4, 1, 1],
        [1, 0, 0, 0, 5, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 1, 0, 0, 5, 0, 1, 6, 0, 3, 1, 0, 7, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


]
level_descriptions = [
    "Level 1: A simple maze to get started. Collect the key and coins to reach the goal.",
    "Level 2: A more challenging layout with multiple doors and a moving enemy.",
    "Level 3: New challenging layout with multiple doors and a moving enemy.",
    "Level 4: You will not be able to pass it cause of the new road",
    "Level 5: Achtung, das ist die herausfordeurung!"
]

# GAME VARIABLE 
current_level = 0
maze = levels[current_level]
unlock = 0
score = 0
game_state = "menu"  # States: "menu", "play", "game_over", "victory"
WIDTH = TILE_SIZE * len(maze[0])
HEIGHT = TILE_SIZE * len(maze)
DEFAULT_WIDTH = TILE_SIZE * len(levels[1][0])  #DEFAULT SIZE OF THE WINDOW
DEFAULT_HEIGHT = TILE_SIZE * len(levels[1])
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
font = pygame.font.Font("Jersey10-Regular.ttf", FONT_SIZE)
enemy_speed_interval = 400  # ENEMY MOVEMENT SPEED
last_enemy_move_time = pygame.time.get_ticks()

#  PLAYER & ENEMY POSITIONS
player = pygame.Rect(TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy = pygame.Rect(3 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy_dir = -1

def update_screen_size(default=False):
    global WIDTH, HEIGHT, TILE_SIZE, screen
    if default:
        WIDTH, HEIGHT = DEFAULT_WIDTH, DEFAULT_HEIGHT
    else:
        WIDTH = TILE_SIZE * len(maze[0])
        HEIGHT = TILE_SIZE * len(maze)

    # Ensure TILE_SIZE is adaptable if needed
    TILE_SIZE = HEIGHT // len(maze) if HEIGHT < WIDTH else WIDTH // len(maze[0])

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

update_screen_size()

def draw():
    screen.fill((0, 0, 0))  # SCREEN COLOR

    # MAZE TILES
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = list(tiles.keys())[maze[row][col]]

            if tile in ['goal', 'door', 'key', 'coin', 'power_up', 'won',]:
                image = pygame.transform.scale(tiles[tile], (TILE_SIZE, TILE_SIZE))
                screen.blit(image, (x, y))
            else:
                color = tiles[tile]
                pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

    # PLAYER & ENEMY IMAGE
    player_image = pygame.image.load("player.png")
    enemy_image = pygame.image.load("enemy.png")

    # Scale images to match TILE_SIZE
    player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
    enemy_image = pygame.transform.scale(enemy_image, (TILE_SIZE, TILE_SIZE))

    # player and enemy
    screen.blit(player_image, (player.x, player.y))
    screen.blit(enemy_image, (enemy.x, enemy.y))

    # SCORES & LEVEL
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {current_level + 1}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()  # Update the display

def move_player(dx, dy):
    global unlock, score, game_state
    row, col = int(player.y // TILE_SIZE), int(player.x // TILE_SIZE)
    new_row, new_col = row + dy, col + dx

    if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
        tile = list(tiles.keys())[maze[new_row][new_col]]
        if tile in ['empty', 'goal', 'key', 'coin', 'power_up', 'won'] or (tile == 'door' and unlock > 0):
            player.x += dx * TILE_SIZE
            player.y += dy * TILE_SIZE

            if tile == 'goal':
                game_state = "victory"
            elif tile == 'won':
                game_state = "won"
            elif tile == 'key':
                unlock += 1
                maze[new_row][new_col] = 0
            elif tile == 'coin':
                score += 10
                maze[new_row][new_col] = 0
            elif tile == 'power_up':
                score += 20
                maze[new_row][new_col] = 0
            elif tile == 'door':
                unlock -= 1
                maze[new_row][new_col] = 0

def move_enemy():
    """Move the enemy at a controlled speed."""
    global game_state, last_enemy_move_time

    # Check if enough time has passed
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_move_time < enemy_speed_interval:
        return

    # Update the last move time
    last_enemy_move_time = current_time

    # Choose a random direction to move
    directions = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0)    # Down
    ]
    random.shuffle(directions)

    row, col = int(enemy.y // TILE_SIZE), int(enemy.x // TILE_SIZE)
    for dx, dy in directions:
        new_row, new_col = row + dy, col + dx
        if (
            0 <= new_row < len(maze) and
            0 <= new_col < len(maze[0]) and
            list(tiles.keys())[maze[new_row][new_col]] != 'wall'
        ):
            enemy.x = new_col * TILE_SIZE
            enemy.y = new_row * TILE_SIZE
            break

    # Check if the enemy collides with the player
    if player.colliderect(enemy):
        game_state = "game_over"

def reset_level():
    global maze, unlock, score, player, enemy, enemy_dir, game_state
    maze = [row[:] for row in levels[current_level]]  # Reload the level from levels
    unlock = 0
    score = 0
    player.topleft = (TILE_SIZE, TILE_SIZE)
    enemy.topleft = (3 * TILE_SIZE, 6 * TILE_SIZE)
    enemy_dir = -1
    game_state = "play"

def next_level():
    global current_level, maze, game_state
    current_level += 1
    if current_level < len(levels):
        maze = levels[current_level]
        reset_level()
        update_screen_size()
    else:
        game_state = "menu"

def show_menu():
    update_screen_size(default=True)

    # FONTS & SIZE OF THE TEXT
    title_font = pygame.font.Font("Jersey10-Regular.ttf", 96)
    subtitle_font = pygame.font.Font("Jersey10-Regular.ttf", 48)
    subtitle1_font = pygame.font.Font("Graduate-Regular.ttf", 24)

    # RENDER TEXT
    main_title_text = title_font.render("Maze Game", True, (255, 255, 255))
    subtitle_text = subtitle_font.render("Main Menu", True, (255, 255, 255))
    subtitle1_text = subtitle1_font.render("© DEVELOPED BY GROUP 3", True, (255, 255, 255))

    # POSITION OF THE TEXT
    main_title_y = 180
    subtitle_y = 280
    subtitle1_y = 650

    # DISPLAY TEXT
    screen.blit(main_title_text, (WIDTH // 2 - main_title_text.get_width() // 2, main_title_y))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, subtitle_y))
    screen.blit(subtitle1_text, (WIDTH // 2 - subtitle1_text.get_width() // 2, subtitle1_y))

    # BUTTONS
    buttons = [
        ("Start Game", start_game),
        ("Levels & Ref", show_levels_page),
        ("Quit", quit_game)
    ]

    # Draw buttons
    draw_buttons(buttons)
    pygame.display.flip()
    
def draw_buttons(buttons):
    buttons_rects = []
    for i, (label, action) in enumerate(buttons):
        # BUTTONSIZES
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 2 + i * 60  # SPACING BETWEEN BUTTONS

        # ROUNDBUTTON
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), button_rect, border_radius=10) #RADIUS OF THE BUTTON

        #ALIGNMENT
        button_text = font.render(label, True, (255, 255, 255))
        text_x = button_rect.centerx - button_text.get_width() // 2
        text_y = button_rect.centery - button_text.get_height() // 2
        screen.blit(button_text, (text_x, text_y))

        buttons_rects.append((button_rect, action))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in buttons_rects:
                    if button.collidepoint(event.pos):
                        action()
                        return

def draw_buttons_independet(buttons):
    buttons_rects = []
    for label, action, (x, y) in buttons:
        # BUTTON SIZES
        button_width, button_height = 200, 50

        # ROUND BUTTON
        button_rect = pygame.Rect(x, y, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), button_rect, border_radius=10)  # RADIUS OF THE BUTTON

        # ALIGNMENT
        button_text = font.render(label, True, (255, 255, 255))
        text_x = button_rect.centerx - button_text.get_width() // 2
        text_y = button_rect.centery - button_text.get_height() // 2
        screen.blit(button_text, (text_x, text_y))

        buttons_rects.append((button_rect, action))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in buttons_rects:
                    if button.collidepoint(event.pos):
                        action()
                        return

def draw_text_multiline(text, font, color, x, y, max_width):
  
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    line_height = font.get_height()
    for i, line in enumerate(lines):
        rendered_text = font.render(line, True, color)
        text_width = rendered_text.get_width()
        screen.blit(rendered_text, (x - text_width // 2, y + i * line_height))

def reference():
    update_screen_size(default=True)

    # FONTS & SIZE OF THE TEXT
    title_font = pygame.font.Font("Jersey10-Regular.ttf", 50)
    subtitle_font = pygame.font.Font("Jersey10-Regular.ttf", 25)
    subtitle1_font = pygame.font.Font("Jersey10-Regular.ttf", 25)
    subtitle2_font = pygame.font.Font("Jersey10-Regular.ttf", 25)
    subtitle3_font = pygame.font.Font("Jersey10-Regular.ttf", 25)

    # RENDER TEXT
    main_title_text = title_font.render("Reference", True, (255, 255, 255))
    subtitle_text = subtitle_font.render("This game, Maze Game has been developed by Group 3.", True, (255, 255, 255))
    subtitle1_text = "The images used within the game, specifically those featuring Tom and Jerry, are referenced for illustrative purposes. However, we do not claim ownership of these images, nor do we assert any copyright over them. These images are used under the understanding that they are publicly available for non-commercial use."
    subtitle2_text = "The title images for the game were sourced from Google.com, with the explicit understanding that these are not under copyright restrictions."
    subtitle3_text = "We acknowledge and respect intellectual property rights and do not intend to infringe on any copyrights by using these images."

    # POSITION OF THE TEXT
    main_title_y = 55
    subtitle_y = 175
    subtitle1_y = 220
    subtitle2_y = 400
    subtitle3_y = 500

    # DISPLAY TEXT
    screen.blit(main_title_text, (WIDTH // 2 - main_title_text.get_width() // 2, main_title_y))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, subtitle_y))
    
    # Draw multiline text with center alignment
    draw_text_multiline(subtitle1_text, subtitle1_font, (255, 255, 255), WIDTH // 2, subtitle1_y, 600)
    draw_text_multiline(subtitle2_text, subtitle2_font, (255, 255, 255), WIDTH // 2, subtitle2_y, 600)
    draw_text_multiline(subtitle3_text, subtitle3_font, (255, 255, 255), WIDTH // 2, subtitle3_y, 600)
    
    # button positions
    buttons = [
        ("Main Menu", show_menu, (WIDTH // 2 - 100, HEIGHT - 100)),
        ("Levels", show_levels_page, (WIDTH // 2 + 150, HEIGHT - 100)),
        ("Quit", quit_game, (WIDTH // 2 - 350, HEIGHT - 100)),
    ]
    draw_buttons_independet(buttons)

    pygame.display.flip()

def show_levels_page():
    update_screen_size(default=True)
    level_images = []

    #LEVELIMAGES
    for i in range(len(level_descriptions)):
        try:
            level_image = pygame.image.load(f'level{i+1}_image.png')  # AUTOUPDATE PF PHOTO
            level_image = pygame.transform.scale(level_image, (415, 320))  # Resize image
            level_images.append(level_image)
        except pygame.error as e:
            print(f"Error loading image for Level {i+1}: {e}")
            level_images.append(None)  # Placeholder for missing image

    while True:
        screen.fill((0, 0, 0))

        # BACKTOMENU BUTTON
        back_button_rect = pygame.Rect(50, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button_rect, border_radius=10) #RADIUS OF THE MENU BUTTON
        back_text = font.render("Back to Menu", True, (255, 255, 255))
        back_text_x = back_button_rect.centerx - back_text.get_width() // 2
        back_text_y = back_button_rect.centery - back_text.get_height() // 2
        screen.blit(back_text, (back_text_x, back_text_y))

        #REFERENCE PAGE
        reference_button_rect = pygame.Rect(50, HEIGHT - 180, 200, 50)
        pygame.draw.rect(screen, (188, 137, 189), reference_button_rect, border_radius=10) #RADIUS OF THE REF BUTTON
        back_text = font.render("Reference", True, (255, 255, 255))
        back_text_x = reference_button_rect.centerx - back_text.get_width() // 2
        back_text_y = reference_button_rect.centery - back_text.get_height() // 2
        screen.blit(back_text, (back_text_x, back_text_y))

        # ALIGNMENTS
        level_buttons = []
        for i, description in enumerate(level_descriptions):
            button_x = 50
            button_y = 50 + i * 60
            button_width, button_height = 200, 50

            level_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, (255, 255, 255), level_button_rect, border_radius=10)

            level_text = font.render(f"Level {i + 1}", True, (0, 0, 0))
            text_x = level_button_rect.centerx - level_text.get_width() // 2
            text_y = level_button_rect.centery - level_text.get_height() // 2
            screen.blit(level_text, (text_x, text_y))

            level_buttons.append((level_button_rect, i))

        # DESCRIPTION
        mouse_pos = pygame.mouse.get_pos()
        for level_button_rect, i in level_buttons:
            if level_button_rect.collidepoint(mouse_pos):
                # DYNAMICTEXT
                dynamic_font_size = max(20, min(30, WIDTH // 40))
                dynamic_font = pygame.font.Font("Jersey10-Regular.ttf", dynamic_font_size)

                # SPLITTING TO PARTS (, TEXT>)
                wrapped_text = []
                words = level_descriptions[i].split(' ')
                line = ""
                for word in words:
                    test_line = f"{line} {word}".strip()
                    if dynamic_font.size(test_line)[0] > WIDTH - 300:  #POS Of text (wrap)
                        wrapped_text.append(line)
                        line = word
                    else:
                        line = test_line
                wrapped_text.append(line) 

                for j, line in enumerate(wrapped_text):
                    description_text = dynamic_font.render(line, True, (255, 255, 255))
                    screen.blit(description_text, (300, 100 + j * (dynamic_font_size + 5)))

                # IMAGE
                if level_images[i]:
                    image = level_images[i]
                    image_rect = image.get_rect(topright=(WIDTH - 100, 200))
                    screen.blit(image, image_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # BUTTONHAPTIC
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    global game_state
                    game_state = "menu"
                    return
                if reference_button_rect.collidepoint(event.pos):
                    game_state = "ref"
                    return

                for level_button_rect, i in level_buttons:
                    if level_button_rect.collidepoint(event.pos):
                        global current_level
                        current_level = i
                        reset_level()
                        return

def start_game():
    update_screen_size(default=True)
    global game_state
    update_screen_size()
    reset_level()
    game_state = "play"

def start_level_1():
    global current_level
    current_level = 0
    reset_level()
    game_state = "play"

def start_level_2():
    global current_level
    current_level = 1
    reset_level()
    game_state = "play"

def start_level_3():
    global current_level
    current_level = 2
    reset_level()
    game_state = "play"

def start_level_4():
    global current_level
    current_level = 3
    reset_level()
    game_state = "play"

def start_level_5():
    global current_level
    current_level = 4
    reset_level()
    game_state = "play"

def quit_game():
    pygame.quit()
    sys.exit()

def show_message(message, options):
    screen.fill((0, 0, 0))
    
    #MESSAGESSIZES
    title_font = pygame.font.Font("Jersey10-Regular.ttf", 48)  #SIZE YOU DIED
    text = title_font.render(message, True, (255, 255, 255))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - 50
    screen.blit(text, (text_x, text_y))
    
    buttons = []
    
    #BUTTONSIZES
    for i, (label, action) in enumerate(options):
        button_width, button_height = 200, 50
        button_x = WIDTH // 2 - button_width // 2
        button_y = HEIGHT // 2 + 60 + i * 60 

        # ROUNDBUTTON
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, (255, 0, 0), button_rect, border_radius=10)

        #ALIGNMENT
        button_text = font.render(label, True, (255, 255, 255))
        text_x = button_rect.centerx - button_text.get_width() // 2
        text_y = button_rect.centery - button_text.get_height() // 2
        screen.blit(button_text, (text_x, text_y))
        
        buttons.append((button_rect, action))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # BUTTON CLICKS THEN DO THIS
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, action in buttons:
                    if button_rect.collidepoint(event.pos):
                        action()  # Calling the corresponding action
                        return

#GAMELOOP
while True:
    if game_state == "ref":
        reference()
    if game_state == "menu":
        show_menu()
    elif game_state == "play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:  # UP / W
                    move_player(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # DOWN / S
                    move_player(0, 1)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # LEFT / A
                    move_player(-1, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # RIGHT / D
                    move_player(1, 0)

        move_enemy()
        draw()
        clock.tick(120) #FPS
    elif game_state == "game_over":
        show_message("You Died!", [("Restart", reset_level), ("Quit", quit_game), ("Menu", show_menu)])
    elif game_state == "victory":
        show_message("Level Completed!", [("Next Level", next_level), ("Main Menu", show_menu)])
    elif game_state == "won":
        show_message("You Did It! Congrats!", [("Main Menu", show_menu), ("Quit", quit_game), ("Reference", reference), ("LVL Descrip", show_levels_page)])