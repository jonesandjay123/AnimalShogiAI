
def get_possible_actions(board, current_player, storage1, storage2, turn_count, con_non_capture_turns, is_game_over):
    raw_actions = []

    for _, piece in board.items():
        if piece.player == current_player:
            available_moves = piece.get_available_moves(board)
            piece_info = (piece.piece_type, piece.coords)
            raw_actions.extend([(piece_info, move) for move in available_moves])

    storage_area = storage1 if current_player == 1 else storage2
    for piece in storage_area:
        available_moves = piece.get_available_moves(board)
        piece_info = (piece.piece_type, piece.coords) if piece.coords else piece.piece_type  # For pieces in storage, they might not have coords
        raw_actions.extend([(piece_info, move) for move in available_moves])

    possible_actions = [{"piece": piece_info, "move": move} for piece_info, move in raw_actions]

    game_info = {
        "turn_count": turn_count,
        "is_game_over": is_game_over,
        "con_non_capture_turns": con_non_capture_turns,
        "possible_actions": possible_actions
    }
    return game_info


def calculate_reward(is_game_over, current_player):
    if is_game_over:
        if current_player == 1:  # 假設玩家1是AI
            return 5  # AI獲勝
        else:
            return -5  # AI失敗
    else:
        return 0  # 遊戲尚未結束或其他情況