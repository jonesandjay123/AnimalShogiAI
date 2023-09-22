from utils import get_cell_coords
from piece import Piece

class RLUitls:
    def __init__(self, game=None):
        self.game = game

    def get_state(self, board, current_player, storage):
        pass

    def get_possible_actions(self, board):
        possible_actions = []

        for cell_name, piece_simple in board['board'].items():
            coords = get_cell_coords(cell_name)
            symbol = piece_simple[0]
            player = piece_simple[1]
            piece = Piece(Piece.piece_type_map[symbol], player, coords, load_image=False)
            available_moves = piece.get_available_moves(board)
            possible_actions.extend([(piece, move) for move in available_moves])
        
        # TODO: piece in storage
        return possible_actions


        # # Step 1 & 2: Find all legal moves for all pieces on the board
        # for piece_location, piece_info in state['board'].items():
        #     for direction in piece_info['valid_moves']:  # Assuming valid_moves is a list of possible directions a piece can move
        #         new_location = get_new_location(piece_location, direction)  # You will need to implement get_new_location
        #         if is_legal_move(new_location, state):  # You will need to implement is_legal_move
        #             possible_actions.append((piece_location, new_location))

        # # Step 3: Include pieces in hand
        # for piece_in_hand in state['storage'][str(state['current_player'])]:
        #     for empty_cell in get_empty_cells(state):  # You will need to implement get_empty_cells to get all empty cells on the board
        #         possible_actions.append(('in_hand', empty_cell))

        return possible_actions

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