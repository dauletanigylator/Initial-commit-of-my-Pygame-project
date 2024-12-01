
import cv2
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
    'goal': (0, 255, 0),       # Green
    'door': (255, 0, 0),       # Red
    'key': (0, 0, 255),        # Blue
    'coin': (255, 215, 0),     # Gold
    'power_up': (255, 0, 255)  # Magenta
}

# LEVELS
levels = [
    #LEVEL2
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 2, 0, 1],
        [1, 0, 1, 0, 1, 1, 3, 1],
        [1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 4, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1],
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
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 5, 0, 3, 1, 0, 0, 2, 0, 3, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 4, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 5, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ] 
]


# Descriptions for levels
level_descriptions = [
    "Level 1: A simple maze to get started. Collect the key and coins to reach the goal.",
    "Level 2: A more challenging layout with multiple doors and a moving enemy.",
    "Level 3: New challenging layout with multiple doors and a moving enemy."
]

# Game variables
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
    global WIDTH, HEIGHT, screen
    if default:
        WIDTH, HEIGHT = DEFAULT_WIDTH, DEFAULT_HEIGHT
    else:
        WIDTH = TILE_SIZE * len(maze[0])
        HEIGHT = TILE_SIZE * len(maze)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


update_screen_size()

def draw():
    screen.fill((0, 0, 0))  # SCREEN COLOUR

    # MAZE TITLES
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            color = tiles[list(tiles.keys())[maze[row][col]]]
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))

    # PLAYER & ENEMY IMAGE
    player_image = pygame.image.load("jerry.png")
    enemy_image = pygame.image.load("tom.png")

    # Scale images to match TILE_SIZE
    player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
    enemy_image = pygame.transform.scale(enemy_image, (TILE_SIZE, TILE_SIZE))

    # PLAYER & ENEMY IMAGE APPEARING
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
        if tile in ['empty', 'goal', 'key', 'coin', 'power_up'] or (tile == 'door' and unlock > 0):
            player.x += dx * TILE_SIZE
            player.y += dy * TILE_SIZE

            if tile == 'goal':
                game_state = "victory"
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
'''

def move_enemy():
    global game_state
    directions = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0)    # Down
    ]
    random.shuffle(directions)  # Randomize movement order
    # Add enemy speed multiplier (0.5 = half speed, 2 = double speed)
    ENEMY_SPEED = 0.5  # Adjust this value to change enemy speed
    
    row, col = int(enemy.y // TILE_SIZE), int(enemy.x // TILE_SIZE)
    
    for dx, dy in directions:
        new_row, new_col = row + dy, col + dx
        if (
            0 <= new_row < len(maze) and 
            0 <= new_col < len(maze[0]) and 
            list(tiles.keys())[maze[new_row][new_col]] != 'wall'
        ):
            # Apply speed multiplier to enemy movement
            enemy.x += dx * TILE_SIZE * ENEMY_SPEED
            enemy.y += dy * TILE_SIZE * ENEMY_SPEED
            break
    # Check if enemy collides with the player
    if player.colliderect(enemy):
        game_state = "game_over"
'''

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
    
    
    #FONTS & SIZE OF THE TEXT
    title_font = pygame.font.Font("Jersey10-Regular.ttf", 96)  
    subtitle_font = pygame.font.Font("Jersey10-Regular.ttf", 48)
    subtitle1_font = pygame.font.Font("Graduate-Regular.ttf", 24)

    #RENDERTEXT
    main_title_text = title_font.render("Maze Game", True, (255, 255, 255))
    subtitle_text = subtitle_font.render("Main Menu", True, (255, 255, 255))
    subtitle1_text = subtitle1_font.render("DEVELOPED BY GROUP 3", True, (255, 255, 255))
    
    #POSITION OF THE TEXT
    main_title_y = 180 
    subtitle_y = 280
    subtitle1_y = 650

    # DISPLAYTEXT
    screen.blit(main_title_text, (WIDTH // 2 - main_title_text.get_width() // 2, main_title_y))
    screen.blit(subtitle_text, (WIDTH // 2 - subtitle_text.get_width() // 2, subtitle_y))
    screen.blit(subtitle1_text, (WIDTH // 2 - subtitle1_text.get_width() // 2, subtitle1_y))

    #BUTTONS
    buttons = [
        ("Start Game", start_game),
        ("Levels", show_levels_page),
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

def show_levels_page():
    update_screen_size(default=True)
    level_images = []

    # Load level images
    for i in range(len(level_descriptions)):
        try:
            level_image = pygame.image.load(f'level{i+1}_image.png')  # Load image for level
            level_image = pygame.transform.scale(level_image, (350, 350))  # Resize image
            level_images.append(level_image)
        except pygame.error as e:
            print(f"Error loading image for Level {i+1}: {e}")
            level_images.append(None)  # Placeholder for missing image

    while True:
        screen.fill((0, 0, 0))

        # BACKTOMENU BUTTON
        back_button_rect = pygame.Rect(50, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button_rect, border_radius=20)
        back_text = font.render("Back to Menu", True, (255, 255, 255))
        back_text_x = back_button_rect.centerx - back_text.get_width() // 2
        back_text_y = back_button_rect.centery - back_text.get_height() // 2
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
                    if dynamic_font.size(test_line)[0] > WIDTH - 300:  #POS Of text
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

                for level_button_rect, i in level_buttons:
                    if level_button_rect.collidepoint(event.pos):
                        global current_level
                        current_level = i
                        reset_level()
                        return
       
def start_game():
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

            # Check if a button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, action in buttons:
                    if button_rect.collidepoint(event.pos):
                        action()  # Call the corresponding action
                        return

#GAMELOOP
while True:
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
        clock.tick(120)
    elif game_state == "game_over":
        show_message("You Died!", [("Restart", reset_level), ("Quit", quit_game), ("Menu", show_menu)])
    elif game_state == "victory":
        show_message("Level Completed!", [("Next Level", next_level), ("Main Menu", show_menu)])