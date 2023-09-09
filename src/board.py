import pygame
from const import DARK_WOOD, LIGHT_WOOD, BLACK, WHITE, ROWS, COLS, SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, WIDTH, HEIGHT


def draw_pieces(window, board_config, storage_area_player1, storage_area_player2):
    for key, value in board_config.items():
        col, row = ord(key[0]) - ord('a'), int(key[1]) - 1
        piece_image = value.image  # Get the already loaded image
        piece_image = pygame.transform.scale(
            piece_image, (SQUARE_SIZE, SQUARE_SIZE))  # Resize the image
        window.blit(piece_image, (GRID_OFFSET_X + col *
                    SQUARE_SIZE, GRID_OFFSET_Y + row * SQUARE_SIZE))

    # Draw the pieces in the storage areas
    storage_cell_size = SQUARE_SIZE * 0.7
    storage_area_start_x = GRID_OFFSET_X - storage_cell_size * 2
    margin = 8  # Adjust the margin as needed

    # Function to draw a piece at a specific storage cell
    def draw_storage_piece(piece, x, y):
        scaled_image = pygame.transform.scale(
            piece.image, (int(SQUARE_SIZE * 0.7), int(SQUARE_SIZE * 0.7)))  # Resize the image
        window.blit(scaled_image, (x, y))

    # Draw pieces in player1's storage area
    for i, piece in enumerate(storage_area_player1):
        x = storage_area_start_x + (i+2) * (storage_cell_size + margin)
        y = GRID_OFFSET_Y + ROWS * SQUARE_SIZE + margin
        draw_storage_piece(piece, x, y)

    # Draw pieces in player2's storage area
    for i, piece in enumerate(storage_area_player2):
        x = storage_area_start_x + (i+2) * (storage_cell_size + margin)
        y = GRID_OFFSET_Y - storage_cell_size - margin
        draw_storage_piece(piece, x, y)


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


def draw_storage_area(window):
    storage_cell_size = SQUARE_SIZE * 0.7
    storage_area_start_x = GRID_OFFSET_X - storage_cell_size * 2
    margin = 8  # Adjust the margin as needed

    # Drawing storage area below the main board
    for i in range(7):  # Adjusted to 7 to match the number of storage cells you wanted
        pygame.draw.rect(window, DARK_WOOD,
                         (storage_area_start_x + i * (storage_cell_size + margin),
                          GRID_OFFSET_Y - storage_cell_size - margin,
                          storage_cell_size, storage_cell_size), 1)

    # Drawing storage area above the main board
    for i in range(7):  # Adjusted to 7 to match the number of storage cells you wanted
        pygame.draw.rect(window, DARK_WOOD,
                         (storage_area_start_x + i * (storage_cell_size + margin),
                          GRID_OFFSET_Y + ROWS * SQUARE_SIZE + margin,
                          storage_cell_size, storage_cell_size), 1)


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
