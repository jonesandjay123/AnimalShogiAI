from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS

def adjust_coordinates_with_offset(x, y, offset_x, offset_y, square_size):
    adjusted_x = (x-1) * square_size + offset_x
    adjusted_y = (y-1) * square_size + offset_y
    return adjusted_x, adjusted_y

def get_storage_cell_details():
    storage_cell_size = SQUARE_SIZE * 0.7
    margin = 8  # Adjust the margin as needed
    return storage_cell_size, margin

def get_grid_coordinates_from_pos(pos):
    """根據給定的像素位置獲得格子座標"""
    x, y = pos
    col = (x - GRID_OFFSET_X) // SQUARE_SIZE
    row = (y - GRID_OFFSET_Y) // SQUARE_SIZE
    return col, row

def get_cell_name_from_pos(pos):
    """根據給定的位置獲取單元格名稱"""
    column_map = {0: "a", 1: "b", 2: "c"}

    col, row = get_grid_coordinates_from_pos(pos)
    
    if 0 <= col <= 2 and 0 <= row <= 3:
        return column_map[col] + str(row + 1)
    else:
        return None  # 返回 None 如果位置不在有效的棋盤範圍內

def get_storage_cell_coords(index, player, storage_cell_size, margin):
    """獲得儲存區的座標"""
    storage_area_start_x = GRID_OFFSET_X - storage_cell_size * 2
    if player == 1:
        y = GRID_OFFSET_Y + ROWS * SQUARE_SIZE + margin
    else:  # player 2
        y = GRID_OFFSET_Y - storage_cell_size - margin
    x = storage_area_start_x + (index+0) * (storage_cell_size + margin)
    return x, y

def get_current_game_state(board_config, storage_area_player1, storage_area_player2, current_player):
    """獲得當前遊戲狀態"""
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

def get_cell_coords(cell_name):
    """獲取單元格名稱的座標"""
    column_map = {"a": 1, "b": 2, "c": 3}
    # 單元格名稱對應a都是從 1 開始的
    column_letter = cell_name[0]
    row_number = int(cell_name[1])

    return column_map[column_letter], row_number

def get_drop_coords(board):
    """獲取所有可打入的空格座標"""
    occupied_coords = {get_cell_coords(key) for key in board.keys()}
    all_coords = {(col, row) for col in range(1, 4) for row in range(1, 5)}
    available_coords = list(all_coords - occupied_coords)

    return available_coords

def get_available_coords(piece):
    """獲得一個棋子的所有可能的移動座標。"""
    # 根據棋子的移動規則來獲得所有可能的移動
    if piece.player == 1:  # 方向 "up"
        possible_moves = piece.get_move_rules()
    else:  # 方向 "down"
        possible_moves = [(-x, -y) for x, y in piece.get_move_rules()]

    # 將可能的移動應用到當前的座標
    current_x, current_y = piece.coords
    possible_moves = [(current_x + x, current_y + y) for x, y in possible_moves]

    return possible_moves

def filter_invalid_moves(player, possible_moves, board):
    """從可落點的座標中過濾掉所有不合法的移動"""
    # 創建一個集合，包含棋盤上所有合法的座標
    all_valid_coords = {(x, y) for x in range(1, 4) for y in range(1, 5)}
    
    # 創建一個集合，其中包含所有目前被同一玩家的其他棋子佔據的座標
    occupied_coords = {piece.coords for piece in board.values() if piece.coords and piece.player == player}

    # 找到所有在棋盤範圍內且未被同一玩家的其他棋子佔據的可能移動
    valid_moves = list(set(possible_moves) & all_valid_coords - occupied_coords)

    return valid_moves

