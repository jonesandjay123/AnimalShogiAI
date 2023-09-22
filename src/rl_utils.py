from utils import get_cell_coords
from piece import Piece


def get_state(self, board, current_player, storage):
    pass

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
        "is_game_over": is_game_over,
        "turn_count": turn_count,
        "con_non_capture_turns": con_non_capture_turns,
        "possible_actions": possible_actions
    }
    return game_info


def calculate_reward(self):
    reward = 0

    # 檢查是否有獅子被吃掉
    if self.is_lion_captured(self.current_player):
        reward -= 5

    # 檢查是否有獅子成功衝到底線
    if self.is_lion_reached_opponent_base(self.current_player):
        reward += 5

    # 檢查遊戲是否勝利
    if self.is_game_won(self.current_player):
        reward += 5

    # ... 你可以根據需要添加更多的規則

    return reward

# 你也需要創建一些額外的輔助方法來檢查特定的遊戲條件，例如：
def is_lion_captured(self, player):
    # 確定是否指定的玩家的獅子被捕捉
    pass

def is_lion_reached_opponent_base(self, player):
    # 確定是否指定的玩家的獅子已經到達對手的基地
    pass

def is_game_won(self, player):
    # 確定指定的玩家是否贏得了遊戲
    pass