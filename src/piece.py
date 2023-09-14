
import pygame
from utils import is_piece_in_storage


piece_type_map = {
    "L": ("Lion", "lion"),
    "G": ("Giraffe", "giraffe"),
    "E": ("Elephant", "elephant"),
    "C": ("Chick", "chick"),
    "H": ("Chicken", "chicken")
}

class Piece:
    def __init__(self, piece_type, player, coords=None):
        self.piece_type = piece_type
        self.player = player
        self.coords = coords

        # Set the name and image file name based on the piece type
        self.name, self.image_file_name = piece_type_map[piece_type]

        # Set the direction based on the player
        self.direction = "up" if player == 1 else "down"

        # Load the image based on the image file name and direction
        self.image = pygame.image.load(
            f"assets/{self.image_file_name}_{self.direction}.png")

        # Set the move rules based on the piece type
        self.move_rules = self.get_move_rules()

    def get_move_rules(self):
        # Define the move rules for each piece type
        move_rules = {
            "L": [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            "G": [(0, 1), (0, -1), (1, 0), (-1, 0)],
            "E": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
            "C": [(0, 1) if self.player == 1 else (0, -1)],
            "H": [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }

        # Get the move rules based on the piece type
        return move_rules[self.piece_type]

    ################################################
    # TODO: 要修改一下裡面get_invalid_moves裡面的bug
    def get_invalid_moves(self, piece, board):
        """找出所有不可移動的格子，包括被其他己方棋子佔據的位置。"""

        invalid_moves = []
        print("piece:", piece)
        print("coords:", piece.coords)
        print("board:", board)

        # for x in range(3):
        #     for y in range(3):
        #         if board[x][y] is not None and board[x][y].player == self.player:
        #             invalid_moves.append((x, y))
        
        return invalid_moves

    def get_available_moves(self, piece, board, storage_area_player1, storage_area_player2):
        """根據棋子的移動規則和棋盤的當前狀態來獲得可用的移動。"""

        # 如果棋子來自存儲區，則返回所有空棋盤格作為可用移動
        if is_piece_in_storage(self, storage_area_player1, storage_area_player2):
            # 這裡您需要一個循環來查找所有空的棋盤格
            available_moves = [(x, y) for x in range(3) for y in range(3) if board[x][y] is None]

        else:
            # 根據棋子的移動規則來獲得所有可能的移動
            if self.player == 1:  # 方向 "up"
                available_moves = self.get_move_rules()
            else:  # 方向 "down"
                available_moves = [(-x, -y) for x, y in self.get_move_rules()]

            # 獲得不可用的移動列表
            not_available_moves = self.get_invalid_moves(piece, board)
            
            # # 創建一個新的列表來存儲最終的可用移動，通過移除所有不可用的移動
            available_moves = [move for move in available_moves if move not in not_available_moves]
        
        return available_moves
        ################################################

    def update_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def update_player(self, new_player):
        # 更新 player 和 direction 屬性
        self.player = new_player
        self.direction = "up" if new_player == 1 else "down"
        
        # 重新加載正確的圖像
        self.image = pygame.image.load(
            f"assets/{self.image_file_name}_{self.direction}.png")
        
        # 更新移動規則，因為它們也可能依賴於 player 屬性
        self.move_rules = self.get_move_rules()

    def update_piece_type(self, new_piece_type):
        self.piece_type = new_piece_type
        # 更新名稱和圖像檔名
        self.name, self.image_file_name = piece_type_map[new_piece_type]

        # 重新加載正確的圖像
        self.image = pygame.image.load(
            f"assets/{self.image_file_name}_{self.direction}.png")

        # 更新移動規則，因為它們也可能依賴於 piece_type 屬性
        self.move_rules = self.get_move_rules()