from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS

def adjust_coordinates_with_offset(x, y, offset_x, offset_y, square_size):
    adjusted_x = x * square_size + offset_x
    adjusted_y = y * square_size + offset_y
    return adjusted_x, adjusted_y

def get_storage_cell_details():
    storage_cell_size = SQUARE_SIZE * 0.7
    margin = 8  # Adjust the margin as needed
    return storage_cell_size, margin


def get_storage_cell_coords(index, player, storage_cell_size, margin):
    storage_area_start_x = GRID_OFFSET_X - storage_cell_size * 2
    if player == 1:
        y = GRID_OFFSET_Y + ROWS * SQUARE_SIZE + margin
    else:  # player 2
        y = GRID_OFFSET_Y - storage_cell_size - margin
    x = storage_area_start_x + (index+0) * (storage_cell_size + margin)
    return x, y

def get_current_game_state(board_config, storage_area_player1, storage_area_player2, current_player):
    game_state = {
        "board": {},
        "storage": {
            1: [],
            -1: []
        },
        "current_player": current_player
    }
    
    # 獲得棋盤的狀態
    for cell_name, piece in board_config.items():
        game_state["board"][cell_name] = (piece.piece_type, piece.player)
    
    # 獲得儲存區的狀態
    for piece in storage_area_player1:
        game_state["storage"][1].append(piece.piece_type)
    
    for piece in storage_area_player2:
        game_state["storage"][-1].append(piece.piece_type)
    
    return game_state

def is_piece_in_storage(piece, storage_area_player1, storage_area_player2):
    """檢查一個棋子是否在存儲區域中。"""
    return piece in storage_area_player1 or piece in storage_area_player2