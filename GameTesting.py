

import pygame
import sys

pygame.init()

TILE_SIZE = 64
WIDTH = TILE_SIZE * 8
HEIGHT = TILE_SIZE * 8

tiles = {
    'empty': (255, 255, 255),  # White
    'wall': (0, 0, 0),         # Black
    'goal': (0, 255, 0),       # Green
    'door': (255, 0, 0),       # Red
    'key': (0, 0, 255)         # Blue
}
unlock = 0

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 2, 0, 1],
    [1, 0, 1, 0, 1, 1, 3, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 4, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 50)

player = pygame.Rect(TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy = pygame.Rect(3 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy_dir = -1

game_state = "playing"  # Can be "playing", "dead", or "won"

def draw():
    screen.fill((0, 0, 0))  # Clear screen with black
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            color = tiles[list(tiles.keys())[maze[row][col]]]
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
    pygame.draw.rect(screen, (255, 255, 0), player)  # Yellow for player
    pygame.draw.rect(screen, (128, 0, 128), enemy)   # Purple for enemy

    if game_state == "dead":
        draw_text("You Died!", (255, 0, 0), WIDTH // 2, HEIGHT // 3)
        draw_button("Restart", (WIDTH // 2, HEIGHT // 2), restart_game)
    elif game_state == "won":
        draw_text("Congratulations! You Passed!", (0, 255, 0), WIDTH // 2, HEIGHT // 3)
        draw_button("Next Level", (WIDTH // 2, HEIGHT // 2), next_level)

    pygame.display.flip()

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_button(text, center, action):
    button_color = (200, 200, 200)
    button_hover_color = (255, 255, 255)
    button_rect = pygame.Rect(0, 0, 200, 50)
    button_rect.center = center

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, button_hover_color, button_rect)
        if mouse_click[0]:
            action()
    else:
        pygame.draw.rect(screen, button_color, button_rect)

    draw_text(text, (0, 0, 0), button_rect.centerx, button_rect.centery)

def restart_game():
    global player, enemy, unlock, game_state
    player.topleft = (TILE_SIZE, TILE_SIZE)
    enemy.topleft = (3 * TILE_SIZE, 6 * TILE_SIZE)
    unlock = 0
    game_state = "playing"

def next_level():
    # replace this with logic for the next level
    print("Next level placeholder!")
    restart_game()

def move_player(dx, dy):
    global unlock, game_state
    if game_state != "playing":
        return

    row, col = int(player.y // TILE_SIZE), int(player.x // TILE_SIZE)
    new_row, new_col = row + dy, col + dx

    if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
        tile = list(tiles.keys())[maze[new_row][new_col]]
        if tile == 'empty' or tile == 'goal' or tile == 'key' or (tile == 'door' and unlock > 0):
            player.x += dx * TILE_SIZE
            player.y += dy * TILE_SIZE
            if tile == 'goal':
                game_state = "won"
            elif tile == 'key':
                unlock += 1
                maze[new_row][new_col] = 0  # Replace with 'empty'
            elif tile == 'door' and unlock > 0:
                unlock -= 1
                maze[new_row][new_col] = 0

def move_enemy():
    global enemy_dir, game_state
    if game_state != "playing":
        return

    row, col = int(enemy.y // TILE_SIZE), int(enemy.x // TILE_SIZE)
    new_row = row + enemy_dir

    if 0 <= new_row < len(maze) and list(tiles.keys())[maze[new_row][col]] != 'wall':
        enemy.y += (enemy_dir * TILE_SIZE) / 2
    else:
        enemy_dir *= -1  # Change direction

    if player.colliderect(enemy):
        game_state = "dead"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_player(0, -1)
            if event.key == pygame.K_DOWN:
                move_player(0, 1)
            if event.key == pygame.K_LEFT:
                move_player(-1, 0)
            if event.key == pygame.K_RIGHT:
                move_player(1, 0)

    move_enemy()
    draw()
    clock.tick(10)
