import pygame
from const import DARK_WOOD, LIGHT_WOOD, BLACK, WHITE, ROWS, COLS, SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, WIDTH, HEIGHT
from piece import Elephant, Lion, Giraffe, Chick


# The initial configuration of the board in terms of pieces
initial_board_config = {
    "b1": Lion('down'),
    "c1": Elephant('down'),
    "b2": Chick('down'),
    "a1": Giraffe('down'),
    "a4": Elephant('up'),
    "b3": Chick('up'),
    "b4": Lion('up'),
    "c4": Giraffe('up'),
}


def create_board():
    board = [
        [None, None, None],
        [None, None, None],
        [None, None, None],
        [None, None, None],
    ]
    for key, value in initial_board_config.items():
        col, row = ord(key[0]) - ord('a'), int(key[1]) - 1
        board[row][col] = value
    return board


def draw_squares(window):
    window.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = LIGHT_WOOD if (row + col) % 2 == 0 else DARK_WOOD
            pygame.draw.rect(window, color, (GRID_OFFSET_X + col * SQUARE_SIZE,
                             GRID_OFFSET_Y + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(window, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                piece.draw(window, row, col)


def draw_grid(window):
    # Draw the grid lines of the board
    for row in range(ROWS + 1):
        pygame.draw.line(window, BLACK,
                         (GRID_OFFSET_X, GRID_OFFSET_Y + row * SQUARE_SIZE),
                         (GRID_OFFSET_X + COLS * SQUARE_SIZE, GRID_OFFSET_Y + row * SQUARE_SIZE), 1)
    for col in range(COLS + 1):
        pygame.draw.line(window, BLACK,
                         (GRID_OFFSET_X + col * SQUARE_SIZE, GRID_OFFSET_Y),
                         (GRID_OFFSET_X + col * SQUARE_SIZE, GRID_OFFSET_Y + ROWS * SQUARE_SIZE), 1)

    # Draw dashed border
    pygame.draw.line(window, BLACK, (0, 0), (WIDTH, 0), 1)
    pygame.draw.line(window, BLACK, (0, 0), (0, HEIGHT), 1)
    pygame.draw.line(window, BLACK, (WIDTH, 0), (WIDTH, HEIGHT), 1)
    pygame.draw.line(window, BLACK, (0, HEIGHT), (WIDTH, HEIGHT), 1)


def draw_labels(window):
    font = pygame.font.SysFont(None, 24)
    # Draw column labels
    labels_col = ['A', 'B', 'C']
    for i, label in enumerate(labels_col):
        label_surface = font.render(label, True, BLACK)
        window.blit(label_surface,
                    (GRID_OFFSET_X + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 10, GRID_OFFSET_Y - 30))
    # Draw row labels
    labels_row = ['1', '2', '3', '4']
    for i, label in enumerate(labels_row):
        label_surface = font.render(label, True, BLACK)
        window.blit(label_surface,
                    (GRID_OFFSET_X - 30, GRID_OFFSET_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2 - 10))


def draw_buttons(window):
    font = pygame.font.Font('assets/NotoSansTC-Bold.ttf', 24)
    button_width, button_height = 60, 40

    # Draw "duel" button
    duel_button = pygame.Rect(
        GRID_OFFSET_X - button_width - 60, HEIGHT // 2 - 60, button_width, button_height)
    pygame.draw.rect(window, LIGHT_WOOD, duel_button)
    duel_label = font.render('對局', True, BLACK)
    window.blit(duel_label, (duel_button.x + 8, duel_button.y + 4))

    # Draw "setup" button
    setup_button = pygame.Rect(
        GRID_OFFSET_X - button_width - 60, HEIGHT // 2 + 20, button_width, button_height)
    pygame.draw.rect(window, LIGHT_WOOD, setup_button)
    setup_label = font.render('擺盤', True, BLACK)
    window.blit(setup_label, (setup_button.x + 8, setup_button.y + 4))
    return duel_button, setup_button
