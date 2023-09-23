import random
from utils import get_possible_actions, get_cell_coords, get_current_game_state, get_cell_name_from_coords
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

    def get_turn_count_val(self):
        return self.turn_count

    def set_turn_count_val(self, count):
        self.turn_count = count

    def generate_possible_actions(self):
        """印出所有可能的行動"""
        # 列印棋盤當前狀態（棋盤觀察）
        game_state = get_current_game_state(self.board_config, self.storage_area_player1, self.storage_area_player2, self.current_player, self.get_turn_count_val())
        # 列印可能的行動（動作空間觀察）
        possible_actions = get_possible_actions(self.board_config, self.current_player, 
            self.storage_area_player1, self.storage_area_player2, self.turn_count, 
            self.con_non_capture_turns, self.game_over)
            # print(game_state)
            # print(possible_actions)
        return game_state, possible_actions

    def select_action(self, possible_actions, epsilon=0.1):
        """選擇棋子"""
        board_piece_possible_actions = possible_actions["board_piece_possible_actions"]
        storage_piece_possible_actions = possible_actions["storage_piece_possible_actions"]

        action_list = board_piece_possible_actions + storage_piece_possible_actions

        print(action_list)

        # Implementing ε-greedy strategy
        rand_num = random.random()  # Generate a random number between 0 and 1
        if rand_num < epsilon:
            # Choose a random action
            selected_action = random.choice(action_list)
        else:
            # Choose the best action - for now, we'll just pick the first one as a placeholder
            # In a real scenario, you'd evaluate the actions using a trained model
            selected_action = action_list[0]
  
        return selected_action
    
    def execute_move(self, new_cell_name, piece_origin):
        """執行移動"""
        # 獲得目標位置上可能存在的棋子
        target_piece = self.board_config.get(new_cell_name)

        print(target_piece)

        # 如果目標位置有一個棋子
        if target_piece:
            # 如果目標棋子是母雞，則降級它
            if target_piece.piece_type == 'H':
                self.toggle_chick_to_hen(target_piece)
            elif target_piece.piece_type == 'L':  # 如果目標棋子是獅子，則宣布遊戲結束
                self.game_over = True

            target_piece.update_player(self.current_player)
            target_piece.coords = None # 座標設置為 None 表示位在存儲區
            
            # 將目標棋子添加到相應的存儲區
            storage_area = self.storage_area_player1 if self.current_player == 1 else self.storage_area_player2
            storage_area.append(target_piece)

        # self.selected_piece.coords = get_cell_coords(new_cell_name)       
        # self.board_config[new_cell_name] = self.selected_piece # 移動選定的棋子到新的位置

        # # 從其原始位置移除選定的棋子
        # if self.selected_piece_origin in self.board_config:
        #     del self.board_config[self.selected_piece_origin]

        # # 給訓練AI看的提醒謎之聲
        # self.ai_cautionary_whisper(self.selected_piece, self.current_player)

        # # 遊戲勝負未揭曉才需要繼續更新下一回合輪到哪位玩家
        # if not self.game_over:
        #     self.update_player_turn()

        # # 更新棋譜
        # self.add_movement_to_notation(self.selected_piece, new_cell_name, piece_origin)

        # # 把狀態空間印出來給ＡＩ看，讓AI知道下一回合要有哪些Actions可以選擇
        # self.show_possible_actions()

        # # 檢查是否變成和棋
        # self.check_draw_condition(target_piece) 

        # # 檢查是否有玩家獲勝
        # self.check_for_winner() 

        # # 列印當前遊戲狀態
        # print(get_current_game_state(self.board_config, self.storage_area_player1, self.storage_area_player2, self.current_player, self.get_turn_count_val()))


    def apply_action(self):
        """應用行動"""
        # Step 1: Check if the action is valid
        _, possible_actions = self.generate_possible_actions()
        action = self.select_action(possible_actions)
        # print(action)
        piece_origin = action['piece'][1]
        new_cell_name = get_cell_name_from_coords(action['move'])
        # print(piece_origin, new_cell_name)
        self.execute_move(new_cell_name, piece_origin)
        

    def toggle_chick_to_hen(self, piece : Piece):
        """將雞轉換為母雞，反之亦然"""
        if piece and piece.piece_type in ["C", "H"]:
            new_piece_type = "H" if piece.piece_type == "C" else "C"
            piece.update_piece_type(new_piece_type)       

    def testRLutils(self):
        self.create_initial_board_config()
        self.apply_action()

    def calculate_reward(self, is_game_over, current_player):
        if is_game_over:
            if current_player == 1:  # 假設玩家1是AI
                return 5  # AI獲勝
            else:
                return -5  # AI失敗
        else:
            return 0  # 遊戲尚未結束或其他情況