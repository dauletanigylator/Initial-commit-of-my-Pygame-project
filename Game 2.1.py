
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
font = pygame.font.SysFont(None, FONT_SIZE)
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
    update_screen_size(default=True)  # Reset to default dimensions
    screen.fill((0, 0, 0))
    title_text = font.render("Main Menu", True, (255, 255, 255))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))

    buttons = [
        ("Start Game", start_game),
        ("Levels", show_levels_page),
        ("Quit", quit_game)
    ]

    draw_buttons(buttons)
    pygame.display.flip()


def draw_buttons(buttons):
    buttons_rects = []
    for i, (label, action) in enumerate(buttons):
        button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + i * 60, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button)
        button_text = font.render(label, True, (255, 255, 255))
        screen.blit(button_text, (button.x + 50, button.y + 10))
        buttons_rects.append((button, action))

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
    # Load images with error checking
    level_images = []
    for i in range(len(level_descriptions)):
        try:
            level_image = pygame.image.load(f'level{i+1}_image.png') #UPLOADING ALL IMAGIES FOR LEVELS
            # Resize the image to make it smaller (e.g., 100px wide)
            level_image = pygame.transform.scale(level_image, (350, 350))  # SIZE OF THE IMAGES
            level_images.append(level_image)
        except pygame.error as e:
            print(f"Error loading image for Level {i+1}: {e}")
            level_images.append(None)  # IF FAILS TEXT NONE

    while True:
        screen.fill((0, 0, 0))
        
        # "Back to Menu" button
        back_button = pygame.Rect(50, HEIGHT - 100, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = font.render("Back to Menu", True, (255, 255, 255))
        screen.blit(back_text, (back_button.x + 25, back_button.y + 15))
        
        # Subpages for levels
        for i, description in enumerate(level_descriptions):
            level_button = pygame.Rect(50, 50 + i * 60, 200, 50)
            pygame.draw.rect(screen, (255, 255, 255), level_button)
            level_text = font.render(f"Level {i + 1}", True, (0, 0, 0))
            screen.blit(level_text, (level_button.x + 50, level_button.y + 10))

            if pygame.mouse.get_pressed()[0] and level_button.collidepoint(pygame.mouse.get_pos()):
                global current_level
                current_level = i
                reset_level()
                return

        # Display description and image for hovered level
        mouse_pos = pygame.mouse.get_pos()
        for i, description in enumerate(level_descriptions):
            level_button = pygame.Rect(50, 50 + i * 60, 200, 50)
            if level_button.collidepoint(mouse_pos):
                # Calculate dynamic font size
                dynamic_font_size = max(30, min(40, WIDTH // 40))
                dynamic_font = pygame.font.Font(None, dynamic_font_size)
                
                # Split text into multiple lines if too wide
                wrapped_text = []
                words = description.split(' ')
                line = ""
                for word in words:
                    test_line = f"{line} {word}".strip()
                    if dynamic_font.size(test_line)[0] > WIDTH - 300:  # Adjust based on available space
                        wrapped_text.append(line)
                        line = word
                    else:
                        line = test_line
                wrapped_text.append(line)  # Add the final line
                
                # Render and display wrapped text
                for j, line in enumerate(wrapped_text):
                    description_text = dynamic_font.render(line, True, (255, 255, 255))
                    screen.blit(description_text, (300, 100 + j * (dynamic_font_size + 5)))

                # Display the image above the description, fitted to the right side
                if level_images[i]:
                    image = level_images[i]  # Get the corresponding image for the level
                    # Position the image on the right side of the screen
                    image_rect = image.get_rect(topright=(WIDTH - 100, 200))  # 50px padding from the right side
                    screen.blit(image, image_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                global game_state
                game_state = "menu"  # Redirect to the main menu
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
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))
    buttons = []
    for i, (label, action) in enumerate(options):
        button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + i * 60, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), button)
        button_text = font.render(label, True, (255, 255, 255))
        screen.blit(button_text, (button.x + 50, button.y + 10))
        buttons.append((button, action))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, action in buttons:
                    if button.collidepoint(event.pos):
                        action()
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