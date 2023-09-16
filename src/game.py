from piece import Piece
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS
from utils import get_cell_name_from_pos, get_grid_coordinates_from_pos, adjust_coordinates_with_offset, get_cell_coords, get_storage_cell_details, get_storage_cell_coords

class Game:
    def __init__(self):
        self.current_player = 1  # 初始化為 1，表示下方玩家、-1 表示上方的玩家
        self.setup_mode = False  # 追蹤是否處於擺盤模式
        self.game_over = False  # 追蹤是否遊戲結束
        self.show_return_to_normal_game_route_button = False # 追蹤是否顯示返回正常遊戲模式的按鈕
        self.mouse_pos = (0, 0) # 追蹤滑鼠位置
        
        self.board_config = {}  # 裡存儲棋盤的當前配置
        self.storage_area_player1 = []
        self.storage_area_player2 = []

        self.selected_piece = None  # 用來追蹤當前選中的棋子
        self.selected_piece_origin = None  # 用來追蹤選中棋子的原始位置
        self.temp_removed_piece = None  # 用來追蹤暫時移除的棋子
        self.available_moves = []  # 當前選中棋子可移動的座標

    def create_initial_board_config(self, start_player=1):
        """初始化為對局模式的配置"""
        self.board_config = {
            "b1": Piece("L", -1, (2, 1)),
            "c1": Piece("E", -1, (3, 1)),
            "b2": Piece("C", -1, (2, 2)),
            "a1": Piece("G", -1, (1, 1)),
            "a4": Piece("E", 1, (1, 4)),
            "b3": Piece("C", 1, (2, 3)),
            "b4": Piece("L", 1, (2, 4)),
        }
        self.current_player = start_player
        self.storage_area_player1 = [Piece("G", 1)]
        self.storage_area_player2 = []

    def click_on_piece(self, pos):
        # 如果遊戲已結束，則直接返回而不進行任何操作
        if self.game_over:
            return
        # 擺盤模式下，只需要處理棋子的選擇
        if self.setup_mode:
            self.select_piece(pos)
        else:
            # 對局模式下，棋子還沒被點擊到游標時，繪製可落點位置
            if self.selected_piece is None:
                self.select_piece(pos)
            else:
                # 根據游標當前棋子的新落點來盤段接續的移動事件
                self.move_event(pos)
                self.available_moves = []

    def select_piece(self, pos):
        """根據給定的位置選擇一個棋子"""
        piece = self.get_piece_at_pos(pos)
        self.available_moves = []
        # 擺盤模式下可以任意選擇棋子，但是對局模式下只能選擇自己的棋子
        if piece and (self.setup_mode or piece.player == self.current_player):
            self.selected_piece = piece
            self.selected_piece_origin = self.get_piece_origin(piece)
            # 儲存暫時移除的棋子
            self.temp_removed_piece = (self.selected_piece, self.selected_piece_origin)
            self.remove_piece_from_origin()  # 立刻從原點移除棋子
            self.mouse_pos = pos  # 更新滑鼠位置

            # 正常對局模式下，還得根據選中的棋子類型跟陣營方向去判斷可能的落子位置
            if not self.setup_mode:
                # 獲得和打印可用移動
                self.available_moves = self.selected_piece.get_available_moves(piece, self.board_config)
                # print(f"Available moves for the selected piece: {self.available_moves}")        


    def get_piece_at_pos(self, pos):
        """根據給定的位置獲取棋子"""
        storage_cell_size, margin = get_storage_cell_details()

        # 檢查玩家 2 的儲存區 然後玩家 1 的儲存區
        for i in range(7):
            x, y = get_storage_cell_coords(i, 2, storage_cell_size, margin)
            if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                # 回傳儲存區的棋子（如果有的話）
                if i < len(self.storage_area_player2):
                    return self.storage_area_player2[i]

        # 檢查玩家 1 的儲存區
        for i in range(7):
            x, y = get_storage_cell_coords(i, 1, storage_cell_size, margin)
            if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                # 回傳儲存區的棋子（如果有的話）
                if i < len(self.storage_area_player1):
                    return self.storage_area_player1[i]

        # 迭代棋盤上的每個單元格，並檢查給定位置是否在單元格的範圍內
        for cell, piece in self.board_config.items():
            cell_x, cell_y = get_cell_coords(cell)
            adjusted_x, adjusted_y = adjust_coordinates_with_offset(cell_x, cell_y, GRID_OFFSET_X, GRID_OFFSET_Y, SQUARE_SIZE)
            if adjusted_x <= pos[0] <= (adjusted_x + SQUARE_SIZE) and adjusted_y <= pos[1] <= (adjusted_y + SQUARE_SIZE):
                return piece
        return None


    def get_piece_origin(self, piece):
        """獲取棋子的原始位置（可以是棋盤上的單元名稱或存儲區域的索引）"""
        for cell_name, board_piece in self.board_config.items():
            if piece == board_piece:
                return cell_name
        for i, storage_piece in enumerate(self.storage_area_player1):
            if piece == storage_piece:
                return ('storage1', i)
        for i, storage_piece in enumerate(self.storage_area_player2):
            if piece == storage_piece:
                return ('storage2', i)
        return None


    def remove_piece_from_origin(self):
        """從原點移除棋子"""
        origin = self.selected_piece_origin
        # 檢驗原點是否在棋盤上
        if isinstance(origin, str):
            del self.board_config[origin]
        # 檢驗原點是否在儲存區
        elif isinstance(origin, tuple):
            if origin[0] == 'storage1':
                self.storage_area_player1.pop(origin[1])
            elif origin[0] == 'storage2':
                self.storage_area_player2.pop(origin[1])


    def return_piece_to_origin(self, piece, origin):
        """將棋子返回到原點"""
        if isinstance(origin, tuple):
            if origin[0] == 'storage1':
                self.storage_area_player1.insert(origin[1], piece)
            else:
                self.storage_area_player2.insert(origin[1], piece)
        else:
            # 若原點是棋盤上的單元格，則將棋子放回原點
            self.board_config[origin] = piece


    def toggle_chick_to_hen(self, piece : Piece):
        """將雞轉換為母雞，反之亦然"""
        if piece and piece.piece_type in ["C", "H"]:
            new_piece_type = "H" if piece.piece_type == "C" else "C"
            piece.update_piece_type(new_piece_type)
            
    def declare_victory(self, player):
        """宣布勝利"""
        player_number = 1 if player == 1 else 2
        print("player", player_number, "wins!!")
        self.game_over = True

    def check_if_reached_opponent_base(self, piece, new_cell_name):
        # 獲得新位置的行數
        _, row_number = get_cell_coords(new_cell_name)

        # 檢查是否達到對手的基線
        if (piece.player == 1 and row_number == 1) or (piece.player == -1 and row_number == 4):
            if piece.piece_type == 'C':  # 如果是小雞，則升級
                self.toggle_chick_to_hen(piece)
            elif piece.piece_type == 'L':  # 如果是獅子，則宣布勝利
                self.declare_victory(piece.player)


    def execute_move(self, new_cell_name, piece_origin):
        """執行移動"""

        if not piece_origin[0].startswith('storage'):
            # 不是從儲存區打入的子才需要檢查是否達到對手的基線
            self.check_if_reached_opponent_base(self.selected_piece, new_cell_name)

        # 獲得目標位置上可能存在的棋子
        target_piece = self.board_config.get(new_cell_name)

        # 如果目標位置有一個棋子，將其移動到相應玩家的存儲區
        if target_piece:
            # 如果目標棋子是母雞，則降級它
            if target_piece.piece_type == 'H':
                self.toggle_chick_to_hen(target_piece)

            target_piece.update_player(self.current_player)
            target_piece.coords = None # 座標設置為 None 表示位在存儲區
            
            # 將目標棋子添加到相應的存儲區
            storage_area = self.storage_area_player1 if self.current_player == 1 else self.storage_area_player2
            storage_area.append(target_piece)

        # 更新棋子的 coords 屬性
        self.selected_piece.coords = get_cell_coords(new_cell_name)

        # 移動選定的棋子到新的位置
        self.board_config[new_cell_name] = self.selected_piece

        # 從其原始位置移除選定的棋子
        if self.selected_piece_origin in self.board_config:
            del self.board_config[self.selected_piece_origin]

        self.update_player_turn()


    def move_event(self, pos):
        """處理棋子的移動事件"""
        grid_x, grid_y = get_grid_coordinates_from_pos(pos)

        # 有當前選定的棋子，因此嘗試將其移動到新位置
        if (grid_x + 1, grid_y + 1) in self.available_moves:
            new_cell_name = get_cell_name_from_pos(pos)
            self.execute_move(new_cell_name, self.selected_piece_origin)
        else:
            # 取得當前被選中棋子的原點
            origin = self.selected_piece_origin
            # 取得當前被選中的棋子
            piece = self.selected_piece
            # 呼叫方法將棋子返回到它的原點
            self.return_piece_to_origin(piece, origin)

        # 重置選定的棋子和原點
        self.selected_piece = None
        self.selected_piece_origin = None


    def update_player_turn(self):
        self.current_player *= -1  # 將玩家 1 切換到 -1，並將 -1 切換到 1


    def toggle_setup_mode(self, go_up):
        self.setup_mode = go_up
        self.show_return_to_normal_game_route_button = False
        self.game_over = False
        print("擺盤按鈕被點擊") if go_up else print("對局按鈕被點擊")