from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS

def adjust_coordinates_with_offset(x, y, offset_x, offset_y, square_size):
    adjusted_x = (x-1) * square_size + offset_x
    adjusted_y = (y-1) * square_size + offset_y
    return adjusted_x, adjusted_y

def get_piece_at_pos(pos, board_config, storage_area_player1, storage_area_player2):
    """根據給定的位置獲取棋子"""
    storage_cell_size, margin = get_storage_cell_details()

    # 檢查玩家 2 的儲存區 然後玩家 1 的儲存區
    for i in range(7):
        x, y = get_storage_cell_coords(i, 2, storage_cell_size, margin)
        if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
            # 回傳儲存區的棋子（如果有的話）
            if i < len(storage_area_player2):
                return storage_area_player2[i]

    # 檢查玩家 1 的儲存區
    for i in range(7):
        x, y = get_storage_cell_coords(i, 1, storage_cell_size, margin)
        if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
            # 回傳儲存區的棋子（如果有的話）
            if i < len(storage_area_player1):
                return storage_area_player1[i]

    # 迭代棋盤上的每個單元格，並檢查給定位置是否在單元格的範圍內
    for cell, piece in board_config.items():
        cell_x, cell_y = get_cell_coords(cell)
        adjusted_x, adjusted_y = adjust_coordinates_with_offset(cell_x, cell_y, GRID_OFFSET_X, GRID_OFFSET_Y, SQUARE_SIZE)
        if adjusted_x <= pos[0] <= (adjusted_x + SQUARE_SIZE) and adjusted_y <= pos[1] <= (adjusted_y + SQUARE_SIZE):
            return piece
    return None

def get_piece_origin(piece, board_config, storage_area_player1, storage_area_player2):
    """獲取棋子的原始位置（可以是棋盤上的單元名稱或存儲區域的索引）"""
    for cell_name, board_piece in board_config.items():
        if piece == board_piece:
            return cell_name
    for i, storage_piece in enumerate(storage_area_player1):
        if piece == storage_piece:
            return ('storage1', i)
    for i, storage_piece in enumerate(storage_area_player2):
        if piece == storage_piece:
            return ('storage2', i)
    return None

def get_storage_cell_details():
    storage_cell_size = SQUARE_SIZE * 0.7
    margin = 8  # Adjust the margin as needed
    return storage_cell_size, margin

def get_grid_coordinates_from_pos(pos):
    """根據給定的像素位置獲得數字座標"""
    x, y = pos
    col = (x - GRID_OFFSET_X) // SQUARE_SIZE
    row = (y - GRID_OFFSET_Y) // SQUARE_SIZE
    return col, row

def get_cell_name_from_pos(pos):
    """根據給定的位置獲取單元格名稱"""
    column_map = {0: "A", 1: "B", 2: "C"}

    col, row = get_grid_coordinates_from_pos(pos)

    if 0 <= col <= 2 and 0 <= row <= 3:
        return column_map[col] + str(row + 1)
    else:
        return None  # 返回 None 如果位置不在有效的棋盤範圍內

def get_cell_name_from_coords(coords):
    """根據給定的座標獲取單元格名稱"""
    column_map = {1: "A", 2: "B", 3: "C"}
    col, row = coords
    return column_map[col] + str(row)

def get_cell_coords(cell_name):
    """獲取單元格名稱的座標"""
    column_map = {"A": 1, "B": 2, "C": 3}
    # 單元格名稱對應a都是從 1 開始的
    column_letter = cell_name[0]
    row_number = int(cell_name[1])

    return column_map[column_letter], row_number

def get_storage_cell_coords(index, player, storage_cell_size, margin):
    """獲得儲存區的座標"""
    storage_area_start_x = GRID_OFFSET_X - storage_cell_size * 2
    if player == 1:
        y = GRID_OFFSET_Y + ROWS * SQUARE_SIZE + margin
    else:  # player 2
        y = GRID_OFFSET_Y - storage_cell_size - margin
    x = storage_area_start_x + (index+0) * (storage_cell_size + margin)
    return x, y

def get_current_game_state(board_config, storage_area_player1, storage_area_player2, current_player, turn_count=None, con_non_capture_turns=None):
    """獲得當前遊戲狀態"""
    game_state = {
        "turn_count": turn_count,
         "current_player": current_player,
        "board": {},
        "storage": {
            "1": [],
            "-1": []
        },
    }
    all_cells = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4"]
    for cell_name in all_cells:
        if cell_name in board_config:
            game_state["board"][cell_name] = [board_config[cell_name].piece_type, board_config[cell_name].player]
        else:
            game_state["board"][cell_name] = [0, 0]  # 表示該位置上沒有棋子

    # 獲得儲存區的狀態
    for piece in storage_area_player1:
        game_state["storage"]["1"].append(piece.piece_type)

    for piece in storage_area_player2:
        game_state["storage"]["-1"].append(piece.piece_type)
    
    return game_state

def get_possible_actions(board, current_player, storage1, storage2, turn_count, con_non_capture_turns, is_game_over):
    board_piece_raw = []
    storage_piece_raw = []
    
    # Get possible actions for board pieces
    for _, piece in board.items():
        if piece.player == current_player:
            available_moves = piece.get_available_moves(board)
            piece_info = (piece.piece_type, piece.coords, get_cell_name_from_coords(piece.coords))
            board_piece_raw.extend([(piece_info, move) for move in available_moves])
    
    # Get possible actions for storage pieces
    storage_area = storage1 if current_player == 1 else storage2
    for piece in storage_area:
        available_moves = piece.get_available_moves(board)
        # piece_info = (piece.piece_type, piece.coords, get_cell_name_from_coords(piece.coords)) if piece.coords else piece.piece_type
        piece_info = (piece.piece_type, piece.coords if piece.coords else None, get_cell_name_from_coords(piece.coords) if piece.coords else None)
        storage_piece_raw.extend([(piece_info, move) for move in available_moves])

    board_piece_possible_actions = [{"piece": piece_info, "move": move} for piece_info, move in board_piece_raw]
    storage_piece_possible_actions = [{"piece": piece_info, "move": move} for piece_info, move in storage_piece_raw]

    game_info = {
        "turn_count": turn_count,
        "is_game_over": is_game_over,
        "con_non_capture_turns": con_non_capture_turns,
        "board_piece_possible_actions": board_piece_possible_actions,
        "storage_piece_possible_actions": storage_piece_possible_actions
    }
    return game_info

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

