import pygame
import pygame_gui
from const import ORANGE_TRANS, DARK_WOOD, LIGHT_WOOD, BLACK, WHITE, ROWS, COLS, SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, WIDTH, HEIGHT
from utils import adjust_coordinates_with_offset, get_storage_cell_details, get_storage_cell_coords


def adjust_coordinates_with_offset(x, y, offset_x, offset_y, square_size):
    adjusted_x = x * square_size + offset_x
    adjusted_y = y * square_size + offset_y
    return adjusted_x, adjusted_y

def draw_pieces(window, board_config, storage_area_player1, storage_area_player2, selected_piece=None, mouse_pos=None):
    for key, value in board_config.items():
        if value == selected_piece:  # Skip drawing the selected piece at its original position
            continue
        col, row = ord(key[0]) - ord('a'), int(key[1]) - 1
        piece_image = value.image  # Get the already loaded image
        piece_image = pygame.transform.scale(
            piece_image, (SQUARE_SIZE, SQUARE_SIZE))  # Resize the image
        x, y = adjust_coordinates_with_offset(col, row, GRID_OFFSET_X, GRID_OFFSET_Y, SQUARE_SIZE)
        window.blit(piece_image, (x, y))

    # Draw the pieces in the storage areas and adjust the margin as needed
    storage_cell_size, margin = get_storage_cell_details()

    # Function to draw a piece at a specific storage cell
    def draw_storage_piece(piece, x, y):
        scaled_image = pygame.transform.scale(
            piece.image, (int(SQUARE_SIZE * 0.7), int(SQUARE_SIZE * 0.7)))  # Resize the image
        window.blit(scaled_image, (x, y))

    # Draw pieces in player2's storage area
    for i, piece in enumerate(storage_area_player2):
        x, y = get_storage_cell_coords(i, 2, storage_cell_size, margin)
        draw_storage_piece(piece, x, y)

    # Draw pieces in player1's storage area
    for i, piece in enumerate(storage_area_player1):
        x, y = get_storage_cell_coords(i, 1, storage_cell_size, margin)
        draw_storage_piece(piece, x, y)

    # Draw the selected piece at the mouse position (if any)
    if selected_piece and mouse_pos:
        piece_image = selected_piece.image
        piece_image = pygame.transform.scale(
            piece_image, (int(SQUARE_SIZE * 1.2), int(SQUARE_SIZE * 1.2)))  # Increase the size of the selected piece
        window.blit(
            piece_image, (mouse_pos[0] - (SQUARE_SIZE * 1.2) // 2, mouse_pos[1] - (SQUARE_SIZE * 1.2) // 2))  # Adjust the position to keep the piece centered on the mouse

def draw_available_moves(window, available_moves):
    for move in available_moves:
        x, y = move
        adjusted_x, adjusted_y = adjust_coordinates_with_offset(x-1, y-1, GRID_OFFSET_X, GRID_OFFSET_Y, SQUARE_SIZE)

        # 計算新的矩形大小
        new_size = int(SQUARE_SIZE * 0.8)
        
        # 計算新的 x 和 y 以使矩形居中
        adjusted_x += (SQUARE_SIZE - new_size) // 2
        adjusted_y += (SQUARE_SIZE - new_size) // 2
        
        # 創建一個半透明的表面
        s = pygame.Surface((new_size, new_size))  
        s.set_alpha(240)  # 設置 alpha 等級
        s.fill(ORANGE_TRANS)  # 設置表面顏色

        # 在正確的位置畫上這個表面
        window.blit(s, (adjusted_x, adjusted_y))


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


def draw_current_player(window, current_player):
    font = pygame.font.Font(None, 36)     # 設定字體和大小
    # 根據當前玩家設定顯示的文字
    text = "Player 1's turn" if current_player == 1 else "Player 2's turn"
    # 生成一個包含文字的表面
    label = font.render(text, 1, DARK_WOOD)
    # 繪製表面到窗口的左上角
    window.blit(label, (10, 10))
    

def draw_buttons(window, show_return_to_game_buttons):
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

    # Draw the "Return to normal game" buttons if show_return_to_game_buttons is True
    if show_return_to_game_buttons:
        # Draw "輪上方走" button
        upper_turn_button = pygame.Rect(
            GRID_OFFSET_X - button_width - 84, HEIGHT // 2 + -80, button_width*1.85, button_height)
        pygame.draw.rect(window, WHITE, upper_turn_button)
        upper_turn_label = font.render('輪上方走', True, BLACK)
        window.blit(upper_turn_label, (upper_turn_button.x + 8, upper_turn_button.y + 4))

        # Draw "輪下方走" button
        lower_turn_button = pygame.Rect(
            GRID_OFFSET_X - button_width - 84, HEIGHT // 2 + -30, button_width*1.85, button_height)
        pygame.draw.rect(window, WHITE, lower_turn_button)
        lower_turn_label = font.render('輪下方走', True, BLACK)
        window.blit(lower_turn_label, (lower_turn_button.x + 8, lower_turn_button.y + 4))
    
    # Return all the buttons as a tuple
    return duel_button, setup_button, upper_turn_button if show_return_to_game_buttons else None, lower_turn_button if show_return_to_game_buttons else None


def draw_control_buttons(window):
    window_height = 560
    board_width = 100
    grid_offset_x = 440

    # 加載圖片
    fast_left_img = pygame.image.load('assets/fast_left.png')
    play_left_img = pygame.image.load('assets/play_left.png')
    play_right_img = pygame.image.load('assets/play_right.png')
    fast_right_img = pygame.image.load('assets/fast_right.png')
    
    # 定義按鈕的位置
    button_y = window_height - 50  # 調整 Y 坐標來定位按鈕
    button_spacing = 60  # 按鈕之間的空間
    
    # 繪製按鈕到視窗上
    window.blit(fast_left_img, (grid_offset_x + board_width + 20, button_y))
    window.blit(play_left_img, (grid_offset_x + board_width + 20 + button_spacing, button_y))
    window.blit(play_right_img, (grid_offset_x + board_width + 20 + button_spacing * 2, button_y))
    window.blit(fast_right_img, (grid_offset_x + board_width + 20 + button_spacing * 3, button_y))

def create_scrolling_container(ui_manager, rect):
    scrolling_container = pygame_gui.elements.UIScrollingContainer(relative_rect=rect, manager=ui_manager)
    # scrolling_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect(0, 0, WIDTH, HEIGHT),
    #                                        manager=ui_manager)
    scrolling_container.set_scrollable_area_dimensions((WIDTH, HEIGHT + 200)) 

    
    labels = []
    original_label_positions = []
    total_scrollable_height = 20 * 30  # 這是我們根據標籤的數量和高度計算的

    # 添加一些臨時標籤來測試滾動容器
    for i in range(20):
        label_rect = pygame.Rect((0, i * 30), (180, 20))
        label = pygame_gui.elements.UILabel(relative_rect=label_rect, text=f'Test Label {i}', manager=ui_manager, container=scrolling_container)
        labels.append(label)
        original_label_positions.append(label_rect.topleft)
    print(original_label_positions)
    # original_label_positions = [(0, i*30) for i in range(20)]
    # for i, pos in enumerate(original_label_positions):
    #     label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((pos[0], pos[1]), (100, 20)),
    #                     text=f"Label {i}",
    #                     manager=ui_manager,
    #                     container=scrolling_container.get_container())  # Add labels to the container
    #     labels.append(label)

    # 定義一個新的矩形來創建滾動條，確保它是在滾動容器的旁邊
    scroll_bar_rect = pygame.Rect((rect.right - 30, rect.y), (30, rect.height))
    vertical_scroll_bar = pygame_gui.elements.UIVerticalScrollBar(relative_rect=scroll_bar_rect, visible_percentage=0.1, manager=ui_manager)
    
    return scrolling_container, vertical_scroll_bar, labels, original_label_positions, total_scrollable_height
