from piece import Piece


class Game:
    def __init__(self):
        self.board_config = {}  # 我們會在這裡存儲棋盤的當前配置
        self.create_initial_board_config()
        self.storage_area_player1 = []
        self.storage_area_player2 = []

    def create_initial_board_config(self):
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

    def initialize_setup_mode(self):
        # 這將清空棋盤，進入擺盤模式
        self.board_config = {}
        self.storage_area_player1 = [Piece("L", 1), Piece(
            "G", 1), Piece("E", 1), Piece("C", 1)]
        self.storage_area_player2 = [
            Piece("L", -1), Piece("G", -1), Piece("E", -1), Piece("C", -1)]
