import json
import random
from const import AUTO_STOP_TERMINATE_TURNS
from utils import get_piece_origin, get_possible_actions, get_cell_coords, get_current_game_state, get_cell_name_from_coords
from piece import Piece

class AnimalShogiEnvLogic:
    def __init__(self):
        self.current_player = 1  # 初始化為 1，表示下方玩家、-1 表示上方的玩家
        self.game_over = False  # 追蹤是否遊戲結束
        self.selected_piece = None  # 用來追蹤當前選中的棋子
        self.selected_piece_origin = None  # 用來追蹤選中棋子的原始位置

        self.turn_count = 0 # 追蹤回合數
        self.con_non_capture_turns = 0 # 追蹤連續無吃子回合數
        self.board_config = {}  # 裡存儲棋盤的當前配置
        self.storage_area_player1 = []
        self.storage_area_player2 = []
        self.board_hist = {}  # 初始化 board_hist 属性
        self.notation_hist = []  # 初始化 notation_hist 属性
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

    def get_con_non_capture_turns_val(self):
        return self.con_non_capture_turns

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

            target_piece.update_player(self.current_player, update_image=False)
            target_piece.coords = None # 座標設置為 None 表示位在存儲區
            
            # 將目標棋子添加到相應的存儲區
            storage_area = self.storage_area_player1 if self.current_player == 1 else self.storage_area_player2
            storage_area.append(target_piece)

        self.selected_piece.coords = get_cell_coords(new_cell_name)       
        self.board_config[new_cell_name] = self.selected_piece # 移動選定的棋子到新的位置

        # 從其原始位置移除選定的棋子
        if self.selected_piece_origin in self.board_config:
            del self.board_config[self.selected_piece_origin]

        # # 給訓練AI看的提醒謎之聲
        # self.ai_cautionary_whisper(self.selected_piece, self.current_player)

        # 遊戲勝負未揭曉才需要繼續更新下一回合輪到哪位玩家
        if not self.game_over:
            self.update_player_turn()

        # # 更新棋譜
        self.add_movement_to_notation(self.selected_piece, new_cell_name, piece_origin)

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
        # 獲得當前遊戲狀態和可能的行動
        _, possible_actions = self.generate_possible_actions()
        action = self.select_action(possible_actions)
        print(action)
        piece_origin = action['piece'][1]
        new_cell_name = get_cell_name_from_coords(action['move'])
        cur_cell_name = get_cell_name_from_coords(piece_origin)
        print(piece_origin, cur_cell_name, new_cell_name)
 
        # 從棋盤上找到選中的棋子
        self.selected_piece = self.board_config[cur_cell_name]
        self.selected_piece_origin = get_piece_origin(self.selected_piece, self.board_config, self.storage_area_player1, self.storage_area_player2)
    
        self.execute_move(new_cell_name, self.selected_piece_origin)
        

    def toggle_chick_to_hen(self, piece : Piece):
        """將雞轉換為母雞，反之亦然"""
        if piece and piece.piece_type in ["C", "H"]:
            new_piece_type = "H" if piece.piece_type == "C" else "C"
            piece.update_piece_type(new_piece_type, update_image=False)       

    def update_player_turn(self):
        """更新下一回合輪到哪位玩家"""
        self.current_player *= -1  # 將玩家 1 切換到 -1，並將 -1 切換到 1

    def update_board_hist(self):
        """把當前局面存進board_hist"""
        current_game_state = get_current_game_state(self.board_config, self.storage_area_player1, self.storage_area_player2, self.current_player, self.get_turn_count_val(), self.get_con_non_capture_turns_val())
        self.board_hist[self.turn_count] = json.dumps(current_game_state)

    def check_if_reached_opponent_base(self, piece, new_cell_name):
        """檢查是否到達對手的基線"""
        _, row_number = get_cell_coords(new_cell_name)
        if (piece.player == 1 and row_number == 1) or (piece.player == -1 and row_number == 4):
            # 如果是小雞且非來自儲存區打入的子，才晉升為母雞
            if piece.piece_type == 'C' and not self.selected_piece_origin[0].startswith('storage'):
                self.toggle_chick_to_hen(piece)
                return True  # 指示晉升發生
            elif piece.piece_type == 'L':  # 如果是獅子衝到底線，則宣布遊戲結束
                self.game_over = True
        return False  # 如果沒有發生晉升，則返回 False

    def generate_notation(self, piece, new_cell_name, piece_origin, turn_count):
        """以記譜規則紀錄當前移動行為"""
        
        # 獲得棋子的類型名稱（例如：'Chick', 'Giraffe' 等）
        piece_name = piece.get_piece_type_display_name()

        is_promoted = self.check_if_reached_opponent_base(piece, new_cell_name)
        
        # 如果棋子是從儲存區打入的，則在棋譜末尾添加單引號（'）
        if piece_origin[0].startswith('storage'):
            notation_suffix = "'"
            notation = f"{new_cell_name}{piece_name}{notation_suffix}"
        elif is_promoted:  # 如果棋子晉升了，則在棋譜末尾添加加號（+）
            notation_suffix = "+"
            notation = f"{new_cell_name}{piece_name}{notation_suffix}({piece_origin})"
        else:  # 如果沒有特殊情況，則記譜後綴為空
            notation_suffix = ""
            notation = f"{new_cell_name}{piece_name}({piece_origin})"
        
        return turn_count + " " + notation

    def add_movement_to_notation(self, piece, new_cell_name, piece_origin):
        """將移動添加到棋譜"""
        self.set_turn_count_val(self.get_turn_count_val() + 1) # 更新回合數

        self.update_board_hist() # 把局面存進board_hist。key是回合數，value是當前局面的JSON字串
        notation = self.generate_notation(piece, new_cell_name, piece_origin, str(self.get_turn_count_val()))
        print(notation)
        self.notation_hist.append(notation) # 把當前回合的棋譜記錄下來


    def testRLutils(self):
        self.create_initial_board_config()
        self.apply_action()

    def check_draw_condition(self, target_piece):
        if self.turn_count >= AUTO_STOP_TERMINATE_TURNS: # 如果走了100步，則宣布遊戲結束
            self.game_over = True

    def calculate_reward(self, is_game_over, current_player):
        if is_game_over:
            if current_player == 1:  # 假設玩家1是AI
                return 5  # AI獲勝
            else:
                return -5  # AI失敗
        else:
            return 0  # 遊戲尚未結束或其他情況