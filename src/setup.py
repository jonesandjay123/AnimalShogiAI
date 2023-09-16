from game import Game
from piece import Piece
from utils import get_cell_name_from_pos, get_current_game_state, get_storage_cell_details, get_storage_cell_coords

class SetupMode:
    def __init__(self, game: Game):
        self.game = game
        

    def initialize_setup_mode(self):
        """初始化擺盤模式"""
        self.game.board_config = {}
        self.game.storage_area_player1 = [Piece("E", 1), Piece("L", 1), Piece("G", 1), Piece("C", 1)]
        self.game.storage_area_player2 = [Piece("E", -1), Piece("L", -1), Piece("G", -1), Piece("C", -1)]


    def place_piece(self, pos):
        """根據給定的位置放置棋子"""
        if self.game.setup_mode and self.game.selected_piece:
            new_cell_name = get_cell_name_from_pos(pos)
            
            if new_cell_name:
                # 檢驗新位置是否已經被佔用
                if self.game.board_config.get(new_cell_name):
                    # 若新位置已經被佔用，則返回棋子到它的原點
                    piece, origin = self.game.temp_removed_piece
                    self.game.return_piece_to_origin(piece, origin)
                    return

                self.game.board_config[new_cell_name] = self.game.selected_piece
                # 重置暫時移除的棋子
                self.game.temp_removed_piece = None
                # 檢查是否兩隻獅子都在棋盤上，並更新標誌以顯示或隱藏轉換選擇按鈕
                self.show_button_when_two_lions()

            else:
                self.handle_piece_placement_in_storage(pos)

            self.game.selected_piece = None
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
            piece, origin = self.game.temp_removed_piece
            self.game.return_piece_to_origin(piece, origin)
        # 檢查是否兩隻獅子都在棋盤上，並更新標誌以顯示或隱藏轉換選擇按鈕
        self.show_button_when_two_lions()

        # 列印當前遊戲狀態
        print(get_current_game_state(self.game.board_config, self.game.storage_area_player1, self.game.storage_area_player2, self.game.current_player))


    def place_piece_in_storage(self, player, index):
        """將棋子放置在儲存區"""
        # 如果棋子是獅子並且它正在被拖到敵人的儲存區，則返回它到原點
        if self.game.selected_piece.name == "Lion" and self.game.selected_piece.player != player:
            piece, origin = self.game.temp_removed_piece
            self.game.return_piece_to_origin(piece, origin)
        else:
            # 如果棋子被拖到敵人的儲存區，則變更其陣營
            if self.game.selected_piece.player != player:
                self.game.selected_piece.update_player(-self.game.selected_piece.player)
            # 當棋子被放置在儲存區時，重置暫時移除的棋子
            self.game.return_piece_to_origin(self.game.selected_piece, ('storage' + str(player), index))    


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
