from game import Game
from piece import Piece
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y
from utils import adjust_coordinates_with_offset, get_current_game_state, get_storage_cell_details, get_storage_cell_coords

class SetupMode:
    def __init__(self, game: Game):
        self.game = game
        self.selected_piece = None  # 用來追蹤當前選中的棋子
        self.selected_piece_origin = None  # 用來追蹤選中棋子的原始位置
        self.temp_removed_piece = None  # 用來追蹤暫時移除的棋子

    def initialize_setup_mode(self):
        """初始化擺盤模式"""
        self.game.board_config = {}
        self.game.storage_area_player1 = [Piece("E", 1), Piece("L", 1), Piece("G", 1), Piece("C", 1)]
        self.game.storage_area_player2 = [Piece("E", -1), Piece("L", -1), Piece("G", -1), Piece("C", -1)]

    def get_piece_at_pos(self, pos):
        """根據給定的位置獲取棋子"""
        storage_cell_size, margin = get_storage_cell_details()

        # 檢查玩家 2 的儲存區 然後玩家 1 的儲存區
        for i in range(7):
            x, y = get_storage_cell_coords(i, 2, storage_cell_size, margin)
            if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                # 回傳儲存區的棋子（如果有的話）
                if i < len(self.game.storage_area_player2):
                    return self.game.storage_area_player2[i]

        # 檢查玩家 1 的儲存區
        for i in range(7):
            x, y = get_storage_cell_coords(i, 1, storage_cell_size, margin)
            if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                # 回傳儲存區的棋子（如果有的話）
                if i < len(self.game.storage_area_player1):
                    return self.game.storage_area_player1[i]

        # 迭代棋盤上的每個單元格，並檢查給定位置是否在單元格的範圍內
        for cell, piece in self.game.board_config.items():
            cell_x, cell_y = self.get_cell_coords(cell)
            adjusted_x, adjusted_y = adjust_coordinates_with_offset(cell_x, cell_y, GRID_OFFSET_X, GRID_OFFSET_Y, SQUARE_SIZE)
            if adjusted_x <= pos[0] <= (adjusted_x + SQUARE_SIZE) and adjusted_y <= pos[1] <= (adjusted_y + SQUARE_SIZE):
                return piece
        return None

    def get_cell_coords(self, cell_name):
        """獲取單元格名稱的座標"""
        column_map = {"a": 0, "b": 1, "c": 2}

        column_letter = cell_name[0]
        # 減去 1 是因為單元格名稱是從 1 開始的，但是列表索引是從 0 開始的
        row_number = int(cell_name[1]) - 1

        return column_map[column_letter], row_number

    def select_piece(self, pos):
        """根據給定的位置選擇一個棋子"""
        piece = self.get_piece_at_pos(pos)

        if piece:
            self.selected_piece = piece
            self.selected_piece_origin = self.get_piece_origin(piece)
            # 儲存暫時移除的棋子
            self.temp_removed_piece = (self.selected_piece, self.selected_piece_origin)
            self.remove_piece_from_origin()  # 立刻從原點移除棋子
            self.mouse_pos = pos  # 更新滑鼠位置

    def get_piece_origin(self, piece):
        """獲取棋子的原始位置（可以是棋盤上的單元名稱或存儲區域的索引）"""
        for cell_name, board_piece in self.game.board_config.items():
            if piece == board_piece:
                return cell_name
        for i, storage_piece in enumerate(self.game.storage_area_player1):
            if piece == storage_piece:
                return ('storage1', i)
        for i, storage_piece in enumerate(self.game.storage_area_player2):
            if piece == storage_piece:
                return ('storage2', i)
        return None

    def place_piece(self, pos):
        """根據給定的位置放置棋子"""
        if self.game.setup_mode and self.selected_piece:
            new_cell_name = self.get_cell_name_from_pos(pos)
            
            if new_cell_name:
                # 檢驗新位置是否已經被佔用
                if self.game.board_config.get(new_cell_name):
                    # 若新位置已經被佔用，則返回棋子到它的原點
                    piece, origin = self.temp_removed_piece
                    self.return_piece_to_origin(piece, origin)
                    return

                self.game.board_config[new_cell_name] = self.selected_piece
                # 重置暫時移除的棋子
                self.temp_removed_piece = None
                # 檢查是否兩隻獅子都在棋盤上，並更新標誌以顯示或隱藏轉換選擇按鈕
                self.show_button_when_two_lions()

            else:
                self.handle_piece_placement_in_storage(pos)

            self.selected_piece = None
            # 當棋子被放置時，重置滑鼠位置
            self.mouse_pos = (0, 0)

            # 列印當前遊戲狀態
            print(get_current_game_state(self.game.board_config, self.game.storage_area_player1, self.game.storage_area_player2, self.game.current_player))


    def handle_piece_placement_in_storage(self, pos):
        """處理棋子放置在儲存區的情況"""
        # 在這裡添加新的檢查來看新位置是否在任一 storage cell
        storage_cell_size, margin = get_storage_cell_details()
        # 初始化一個變量來跟踪是否找到了一個有效的儲存單元格
        valid_storage_cell_found = False
        # 檢查每個 player 的每個 storage cell
        for player in [1, -1]:
            for index in range(7):  # 假設有7個 storage cells
                # 獲得當前 cell 的座標
                x, y = get_storage_cell_coords(index, player, storage_cell_size, margin)
                
                # 檢查新位置是否在這個 cell 的範圍內
                if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                    # 如果在，則進行相應的操作
                    # print(f"Piece placed in storage cell: Player {player}, Index {index}")
                    
                    # 處理在儲存區的棋子放置
                    self.place_piece_in_storage(player, index)
                    valid_storage_cell_found = True
                    break  # 當找到匹配的 cell 時跳出循环
            # 如果已經找到一個有效的儲存單元格，則退出循環
            if valid_storage_cell_found:
                break
        # 如果沒有找到任何有效的儲存單元格，則返回棋子到它的原點
        if not valid_storage_cell_found:
            piece, origin = self.temp_removed_piece
            self.return_piece_to_origin(piece, origin)
        # 檢查是否兩隻獅子都在棋盤上，並更新標誌以顯示或隱藏轉換選擇按鈕
        self.show_button_when_two_lions()

        # 列印當前遊戲狀態
        print(get_current_game_state(self.game.board_config, self.game.storage_area_player1, self.game.storage_area_player2, self.game.current_player))

    def place_piece_in_storage(self, player, index):
        """將棋子放置在儲存區"""
        # 如果棋子是獅子並且它正在被拖到敵人的儲存區，則返回它到原點
        if self.selected_piece.name == "Lion" and self.selected_piece.player != player:
            piece, origin = self.temp_removed_piece
            self.return_piece_to_origin(piece, origin)
        else:
            # 如果棋子被拖到敵人的儲存區，則變更其陣營
            if self.selected_piece.player != player:
                self.selected_piece.update_player(-self.selected_piece.player)
            # 當棋子被放置在儲存區時，重置暫時移除的棋子
            self.return_piece_to_origin(self.selected_piece, ('storage' + str(player), index))
            

    def get_cell_name_from_pos(self, pos):
        """根據給定的位置獲取單元格名稱"""
        column_map = {0: "a", 1: "b", 2: "c"}

        x, y = pos
        column = (x - GRID_OFFSET_X) // SQUARE_SIZE
        row = (y - GRID_OFFSET_Y) // SQUARE_SIZE

        if 0 <= column <= 2 and 0 <= row <= 3:
            return column_map[column] + str(row + 1)
        else:
            return None  # 返回 None 如果位置不在有效的棋盤範圍內

    def remove_piece_from_origin(self):
        """從原點移除棋子"""
        origin = self.selected_piece_origin
        # 檢驗原點是否在棋盤上
        if isinstance(origin, str):
            del self.game.board_config[origin]
        # 檢驗原點是否在儲存區
        elif isinstance(origin, tuple):
            if origin[0] == 'storage1':
                removed_piece = self.game.storage_area_player1.pop(origin[1])
            elif origin[0] == 'storage2':
                removed_piece = self.game.storage_area_player2.pop(origin[1])

    def return_piece_to_origin(self, piece, origin):
        """將棋子返回到原點"""
        if isinstance(origin, tuple):
            if origin[0] == 'storage1':
                self.game.storage_area_player1.insert(origin[1], piece)
            else:
                self.game.storage_area_player2.insert(origin[1], piece)
        else:
            # 若原點是棋盤上的單元格，則將棋子放回原點
            self.game.board_config[origin] = piece

    def toggle_chick_to_hen(self, piece : Piece):
        """將雞轉換為母雞，反之亦然"""
        if piece and piece.piece_type in ["C", "H"]:
            new_piece_type = "H" if piece.piece_type == "C" else "C"
            piece.update_piece_type(new_piece_type)
            # 列印當前遊戲狀態
            print(get_current_game_state(self.game.board_config, self.game.storage_area_player1, self.game.storage_area_player2, self.game.current_player))

    def show_button_when_two_lions(self):
        """檢查是否兩隻獅子都在棋盤上，並更新標誌以顯示或隱藏轉換選擇按鈕"""
        lion_count = sum(1 for piece in self.game.board_config.values() if piece.piece_type == "L")
        self.game.show_return_to_normal_game_route_button = lion_count == 2
