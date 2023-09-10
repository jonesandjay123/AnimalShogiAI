from piece import Piece
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
from utils import adjust_coordinates_with_offset, get_storage_cell_details, get_storage_cell_coords

class SetupMode:
    def __init__(self):
        self.setup_mode = False  # 追蹤是否處於擺盤模式
        self.show_return_to_normal_game_route_button = False # 追蹤是否顯示返回正常遊戲模式的按鈕
        self.board_config = {}  # 我們會在這裡存儲棋盤的當前配置
        self.storage_area_player1 = []
        self.storage_area_player2 = []
        self.selected_piece = None  # 用來追蹤當前選中的棋子
        self.selected_piece_origin = None  # 用來追蹤選中棋子的原始位置
        self.temp_removed_piece = None  # 用來追蹤暫時移除的棋子


    def initialize_setup_mode(self):
        self.board_config = {}
        self.storage_area_player1 = [Piece("E", 1), Piece("L", 1), Piece("G", 1), Piece("C", 1)]
        self.storage_area_player2 = [Piece("E", -1), Piece("L", -1), Piece("G", -1), Piece("C", -1)]
