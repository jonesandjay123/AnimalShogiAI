
import pygame
from utils import get_drop_coords, get_available_coords, filter_invalid_moves

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
        self.direction = "up" if player == 1 else "down"
        self.move_rules = self.get_move_rules()
        self.load_image()

    def load_image(self):
        self.image = pygame.image.load(
            f"assets/{self.image_file_name}_{self.direction}.png")

    def get_move_rules(self):
        """根據棋子的類型來獲得偏移量值。"""
        move_rules = {
            "L": [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            "G": [(0, 1), (0, -1), (1, 0), (-1, 0)],
            "E": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
            "C": [(0, -1)], # 往上移動的動作在棋盤上是-1，因為y軸是上小下大。前面的子由於走位都是對稱的，所以不受影響。
            "H": [(0, 1), (0, -1), (-1, 0), (1, 0), (1, -1), (-1, -1)] # 同上邏輯，y軸向上移是-1。
        }
        return move_rules[self.piece_type]

    def get_available_moves(self, piece, board):
        """根據棋子的移動規則和棋盤的當前狀態來獲得可用的移動。"""
        # 如果coords是None表示它來自存儲區，則返回所有空棋盤格作為可被打入的座標位置
        if not piece.coords:
            available_moves = get_drop_coords(board)
        else:
            possible_moves = get_available_coords(piece)
            available_moves = filter_invalid_moves(piece.player, possible_moves, board)
        return available_moves

    def update_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def update_player(self, new_player):
        # 更新 player 和 direction 屬性
        self.player = new_player
        self.direction = "up" if new_player == 1 else "down"
        
        # 重新加載正確的圖像
        self.load_image()
        
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