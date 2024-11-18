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
clock = pygame.time.Clock()

player = pygame.Rect(TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy = pygame.Rect(3 * TILE_SIZE, 6 * TILE_SIZE, TILE_SIZE, TILE_SIZE)
enemy_dir = -1

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
    pygame.display.flip()

def move_player(dx, dy):
    global unlock
    row, col = int(player.y // TILE_SIZE), int(player.x // TILE_SIZE)
    new_row, new_col = row + dy, col + dx

    if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]):
        tile = list(tiles.keys())[maze[new_row][new_col]]
        if tile == 'empty' or tile == 'goal' or tile == 'key' or (tile == 'door' and unlock > 0):
            player.x += dx * TILE_SIZE
            player.y += dy * TILE_SIZE
            if tile == 'goal':
                print("Well done!")
                pygame.quit()
                sys.exit()
            elif tile == 'key':
                unlock += 1
                maze[new_row][new_col] = 0  # Replace with 'empty'
            elif tile == 'door' and unlock > 0:
                unlock -= 1
                maze[new_row][new_col] = 0

def move_enemy():
    global enemy_dir
    row, col = int(enemy.y // TILE_SIZE), int(enemy.x // TILE_SIZE)
    new_row = row + enemy_dir

    if 0 <= new_row < len(maze) and list(tiles.keys())[maze[new_row][col]] != 'wall':
        enemy.y += (enemy_dir * TILE_SIZE)/2
    else:
        enemy_dir *= -1  # Change direction

    if player.colliderect(enemy):
        print("You died!")
        pygame.quit()
        sys.exit()

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
