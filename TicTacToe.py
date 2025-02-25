import pygame
import sys

pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 306, 406
BG_COLOR = (228, 228, 228)
LINE_COLOR = (237, 215, 186)
FONT_COLOR = (30, 216, 108)
RESTART_BG_COLOR = (30, 216, 108)
CELL_COLOR = (58, 60, 62)
CELL_HOVER_COLOR = (4, 192, 178)

# Game Variables
game_active = True
current_player = "X"
game_state = [""] * 9
winner = None
cell_size = 100
grid_pos = (0, 100)

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
font = pygame.font.Font(None, 60)
restart_font = pygame.font.Font(None, 25)
clock = pygame.time.Clock()

# Function to draw the grid
def draw_grid():
    for row in range(3):
        for col in range(3):
            cell_rect = pygame.Rect(col * (cell_size + 2), grid_pos[1] + row * (cell_size + 2), cell_size, cell_size)
            pygame.draw.rect(screen, LINE_COLOR, cell_rect, 3)

# Function to draw the game state
def draw_game_state():
    for index, player in enumerate(game_state):
        if player:
            row, col = divmod(index, 3)
            text_surf = font.render(player, True, FONT_COLOR)
            text_rect = text_surf.get_rect(center=(col * (cell_size + 2) + cell_size // 2, grid_pos[1] + row * (cell_size + 2) + cell_size // 2))
            screen.blit(text_surf, text_rect)

# Function to check for game over
def check_game_over():
    global game_active, winner
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
        [0, 4, 8], [2, 4, 6]             # Diagonal
    ]
    
    for condition in win_conditions:
        if game_state[condition[0]] == game_state[condition[1]] == game_state[condition[2]] != "":
            winner = current_player
            game_active = False
            break
    else:
        if "" not in game_state:
            winner = "Draw"
            game_active = False

# Function to restart the game
def restart_game():
    global game_state, game_active, current_player, winner
    game_state = [""] * 9
    game_active = True
    current_player = "X"
    winner = None

# Main game loop
while True:
    screen.fill(BG_COLOR)
    draw_grid()
    draw_game_state()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and game_active:
            x, y = pygame.mouse.get_pos()
            if y > 100:  # Click is within grid
                col, row = x // (cell_size + 2), (y - 100) // (cell_size + 2)
                cell_index = row * 3 + col
                if game_state[cell_index] == "":
                    game_state[cell_index] = current_player
                    check_game_over()
                    current_player = "O" if current_player == "X" else "X"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                restart_game()
                
    if not game_active:
        restart_surf = restart_font.render('Press Space to Restart', True, FONT_COLOR)
        screen.blit(restart_surf, (50, 30))
        
    pygame.display.flip()
    clock.tick(60)