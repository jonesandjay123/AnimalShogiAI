from piece import Piece
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS

class Game:
    def __init__(self):
        self.current_player = 1  # 初始化為 1，表示下方玩家、-1 表示上方的玩家
        self.setup_mode = False  # 追蹤是否處於擺盤模式
        self.show_return_to_normal_game_route_button = False # 追蹤是否顯示返回正常遊戲模式的按鈕
        self.board_config = {}  # 我們會在這裡存儲棋盤的當前配置
        self.storage_area_player1 = []
        self.storage_area_player2 = []
        # Add this line to initialize the mouse position
        self.mouse_pos = (0, 0)

    def create_initial_board_config(self):
        """初始化為對局模式的配置"""
        self.board_config = {
            "b1": Piece("L", -1),
            "c1": Piece("E", -1),
            "b2": Piece("C", -1),
            "a1": Piece("G", -1),
            "a4": Piece("E", 1),
            "b3": Piece("C", 1),
            "b4": Piece("L", 1),
            "c4": Piece("G", 1),
        }
        self.storage_area_player1 = []
        self.storage_area_player2 = []

    def end_turn(self):
        self.current_player *= -1  # 將玩家 1 切換到 -1，並將 -1 切換到 1