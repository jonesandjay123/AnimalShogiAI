from piece import Elephant, Lion, Giraffe, Chick


class Game:
    def __init__(self):
        self.board_config = {}  # 我們會在這裡存儲棋盤的當前配置
        self.create_initial_board_config()

    def create_initial_board_config(self):
        self.board_config = {
            "b1": Lion('down'),
            "c1": Elephant('down'),
            "b2": Chick('down'),
            "a1": Giraffe('down'),
            "a4": Elephant('up'),
            "b3": Chick('up'),
            "b4": Lion('up'),
            "c4": Giraffe('up'),
        }

    def initialize_setup_mode(self):
        # 這將清空棋盤，進入擺盤模式
        self.board_config = {}
