from piece import Piece
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS
from utils import adjust_coordinates_with_offset, get_cell_coords, get_storage_cell_details, get_storage_cell_coords

class Game:
    def __init__(self):
        self.current_player = 1  # 初始化為 1，表示下方玩家、-1 表示上方的玩家
        self.setup_mode = False  # 追蹤是否處於擺盤模式
        self.show_return_to_normal_game_route_button = False # 追蹤是否顯示返回正常遊戲模式的按鈕
        self.mouse_pos = (0, 0) # 追蹤滑鼠位置
        
        self.board_config = {}  # 裡存儲棋盤的當前配置
        self.storage_area_player1 = []
        self.storage_area_player2 = []

        self.selected_piece = None  # 用來追蹤當前選中的棋子
        self.selected_piece_origin = None  # 用來追蹤選中棋子的原始位置
        self.temp_removed_piece = None  # 用來追蹤暫時移除的棋子

    def create_initial_board_config(self):
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
        self.storage_area_player1 = [Piece("G", 1)]
        self.storage_area_player2 = []

    def select_piece(self, pos):
        """根據給定的位置選擇一個棋子"""
        piece = self.get_piece_at_pos(pos)
        available_moves = []
        if piece:
            self.selected_piece = piece
            self.selected_piece_origin = self.get_piece_origin(piece)
            # 儲存暫時移除的棋子
            self.temp_removed_piece = (self.selected_piece, self.selected_piece_origin)
            self.remove_piece_from_origin()  # 立刻從原點移除棋子
            self.mouse_pos = pos  # 更新滑鼠位置

            # 正常對局模式下，還得根據選中的棋子類型跟陣營方向去判斷可能的落子位置
            if not self.setup_mode:
                # 獲得和打印可用移動
                available_moves = self.selected_piece.get_available_moves(piece, self.board_config)
                print(f"Available moves for the selected piece: {available_moves}")        
        return available_moves

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
                removed_piece = self.storage_area_player1.pop(origin[1])
            elif origin[0] == 'storage2':
                removed_piece = self.storage_area_player2.pop(origin[1])

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

    def end_turn(self):
        self.current_player *= -1  # 將玩家 1 切換到 -1，並將 -1 切換到 1