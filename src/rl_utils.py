from utils import get_possible_actions, get_cell_coords, get_current_game_state
from piece import Piece

class AnimalShogiEnvLogic:
    def __init__(self):
        self.current_player = 1  # 初始化為 1，表示下方玩家、-1 表示上方的玩家
        self.game_over = False  # 追蹤是否遊戲結束

        self.turn_count = 0 # 追蹤回合數
        self.con_non_capture_turns = 0 # 追蹤連續無吃子回合數
        self.board_config = {}  # 裡存儲棋盤的當前配置
        self.storage_area_player1 = []
        self.storage_area_player2 = []
        self.board_hist = {}  # 初始化 board_hist 属性
        self.available_moves = []  # 當前選中棋子可移動的座標
    
    def default_board_config(self):
        return {
            "B1": Piece("L", -1, None, False),
            "C1": Piece("E", -1, None, False),
            "B2": Piece("C", -1, None, False),
            "A1": Piece("G", -1, None, False),
            "A4": Piece("E", 1, None, False),
            "B3": Piece("C", 1, None, False),
            "B4": Piece("L", 1, None, False),
            "C4": Piece("G", 1, None, False)
        }

    def create_initial_board_config(self, start_player=1):
        """初始化為對局模式的配置"""
        self.board_config = self.default_board_config()
        self.current_player = start_player
        self.storage_area_player1 = []
        self.storage_area_player2 = []

        self.rescan_piece_coords() # 重設掃描棋子座標
        self.generate_possible_actions() # 把狀態空間印出來給ＡＩ看

    def rescan_piece_coords(self):
        # 重設暫存屬性
        self.turn_count = 0
        self.available_moves = []

        # 更新每個棋子的 coords 屬性
        for cell_name, piece in self.board_config.items():
            piece.coords = get_cell_coords(cell_name) # 幫每個棋子標上對應的coords座標

    def generate_possible_actions(self):
        """印出所有可能的行動"""
        # 列印棋盤當前狀態（棋盤觀察）
        game_state = get_current_game_state(self.board_config, self.storage_area_player1, self.storage_area_player2, self.current_player, self.get_turn_count_val())
        # 列印可能的行動（動作空間觀察）
        possible_actions = get_possible_actions(self.board_config, self.current_player, 
            self.storage_area_player1, self.storage_area_player2, self.turn_count, 
            self.con_non_capture_turns, self.game_over)
        print(game_state)
        print(possible_actions)
        return game_state, possible_actions

    def calculate_reward(self, is_game_over, current_player):
        if is_game_over:
            if current_player == 1:  # 假設玩家1是AI
                return 5  # AI獲勝
            else:
                return -5  # AI失敗
        else:
            return 0  # 遊戲尚未結束或其他情況