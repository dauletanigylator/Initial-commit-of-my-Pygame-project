
import pygame
import sys

pygame.init()

TILE_SIZE = 80
FONT_SIZE = 32

# Define colors for tiles
tiles = {
    'empty': (255, 255, 255),  # White
    'wall': (0, 0, 0),         # Black
    'goal': (0, 255, 0),       # Green
    'door': (255, 0, 0),       # Red
    'key': (0, 0, 255),        # Blue
    'coin': (255, 215, 0),     # Gold
    'power_up': (255, 0, 255)  # Magenta
}

# Define levels
levels = [
    # Level 1
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
    # Level 2
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
    ]
]

# Descriptions for levels
level_descriptions = [
    "Level 1: A simple maze to get started. Collect the key and coins to reach the goal.",
    "Level 2: A more challenging layout with multiple doors and a moving enemy."
]

# Game variables
current_level = 0
maze = levels[current_level]
unlock = 0
score = 0
game_state = "menu"  # States: "play", "game_over", "victory", "menu", "levels"

# Dynamic screen size
def update_screen_size():
    global WIDTH, HEIGHT
    WIDTH = TILE_SIZE * len(maze[0])
    HEIGHT = TILE_SIZE * len(maze)
    pygame.display.set_mode((WIDTH, HEIGHT))

update_screen_size()

# Initialize Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

# Initialize player and enemy positions
player = pygame.Rect(TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy = pygame.Rect(3 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy_dir = -1


def draw():
    screen.fill((0, 0, 0))
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            color = tiles[list(tiles.keys())[maze[row][col]]]
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, (255, 255, 0), player)  # Yellow for player
    pygame.draw.rect(screen, (128, 0, 128), enemy)   # Purple for enemy

    # Display score and level
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {current_level + 1}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()


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
    global enemy_dir, game_state
    row, col = int(enemy.y // TILE_SIZE), int(enemy.x // TILE_SIZE)
    new_row = row + enemy_dir

    if 0 <= new_row < len(maze) and list(tiles.keys())[maze[new_row][col]] != 'wall':
        enemy.y = new_row * TILE_SIZE
    else:
        enemy_dir *= -1

    if player.colliderect(enemy):
        game_state = "game_over"


def reset_level():
    global maze, unlock, score, player, enemy, enemy_dir, game_state
    maze = levels[current_level]
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


def show_levels_page():
    while True:
        screen.fill((0, 0, 0))
        
        # Draw "Back to Menu" button
        back_button = pygame.Rect(50, HEIGHT - 80, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = font.render("Back to Menu", True, (255, 255, 255))
        screen.blit(back_text, (back_button.x + 20, back_button.y + 10))
        
        # Draw subpages for levels
        for i, description in enumerate(level_descriptions):
            level_button = pygame.Rect(50, 50 + i * 60, 200, 50)
            pygame.draw.rect(screen, (0, 255, 0), level_button)
            level_text = font.render(f"Level {i + 1}", True, (0, 0, 0))
            screen.blit(level_text, (level_button.x + 50, level_button.y + 10))

            if pygame.mouse.get_pressed()[0] and level_button.collidepoint(pygame.mouse.get_pos()):
                global current_level
                current_level = i
                reset_level()
                return

        # Display description of hovered level
        mouse_pos = pygame.mouse.get_pos()
        for i, description in enumerate(level_descriptions):
            level_button = pygame.Rect(50, 50 + i * 60, 200, 50)
            if level_button.collidepoint(mouse_pos):
                description_text = font.render(description, True, (255, 255, 255))
                screen.blit(description_text, (300, 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                return


def show_message(message, buttons):
    global game_state
    while True:
        screen.fill((0, 0, 0))
        text = font.render(message, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

        button_rects = []
        for i, (label, action) in enumerate(buttons):
            button_rect = pygame.Rect(WIDTH // 2 - 100, 150 + i * 60, 200, 50)
            pygame.draw.rect(screen, (0, 255, 0), button_rect)
            button_text = font.render(label, True, (0, 0, 0))
            screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))
            button_rects.append((button_rect, action))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, action in button_rects:
                    if button_rect.collidepoint(event.pos):
                        action()
                        return

# Main Game Loop
while True:
    if game_state == "menu":
        show_message("Main Menu", [("Play", reset_level), ("Levels", show_levels_page), ("Quit", sys.exit)])
    elif game_state == "play":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)

        move_enemy()
        draw()
        clock.tick(60)
    elif game_state == "victory":
        next_level()
    elif game_state == "game_over":
        show_message("Game Over", [("Restart", reset_level), ("Menu", lambda: setattr(game_state, "menu"))])
