from piece import Piece
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y, ROWS
from utils import get_storage_cell_details, get_storage_cell_coords


class Game:
    def __init__(self):
        self.setup_mode = False  # 追蹤蹤是否處於擺盤模式
        self.board_config = {}  # 我們會在這裡存儲棋盤的當前配置
        self.create_initial_board_config()
        self.storage_area_player1 = []
        self.storage_area_player2 = []
        self.selected_piece = None  # 用來追蹤當前選中的棋子
        self.selected_piece_origin = None  # 用來追蹤選中棋子的原始位置
        self.temp_removed_piece = None  # 用來追蹤暫時移除的棋子
        # Add this line to initialize the mouse position
        self.mouse_pos = (0, 0)

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
        self.storage_area_player1 = [Piece(
            "E", 1), Piece("L", 1), Piece("G", 1), Piece("C", 1)]
        self.storage_area_player2 = [
            Piece("E", -1), Piece("L", -1), Piece("G", -1), Piece("C", -1)]

    def get_piece_at_pos(self, pos):
        print(f"Checking pos: {pos}")

        # check the storage areas and adjust the margin as needed
        storage_cell_size, margin = get_storage_cell_details()

        # First check player2's storage area, then check player1's.
        for i in range(7):
            x, y = get_storage_cell_coords(i, 2, storage_cell_size, margin)
            if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                # Return the piece at this storage cell if any
                if i < len(self.storage_area_player2):
                    print(
                        f"Checking storage cell index: {i}, Player: 2, Cell coords: {(x, y)}, Piece: {self.storage_area_player2[i]}")
                    return self.storage_area_player2[i]

        # Check player1's storage area
        for i in range(7):
            x, y = get_storage_cell_coords(i, 1, storage_cell_size, margin)
            if x <= pos[0] <= x + storage_cell_size and y <= pos[1] <= y + storage_cell_size:
                # Return the piece at this storage cell if any
                if i < len(self.storage_area_player1):
                    print(
                        f"Checking storage cell index: {i}, Player: 1, Cell coords: {(x, y)}, Piece: {self.storage_area_player1[i]}")
                    return self.storage_area_player1[i]

        # Iterate over the board configuration to find if a piece is at the current position
        for cell, piece in self.board_config.items():
            cell_x, cell_y = self.get_cell_coords(cell)
            if cell_x * SQUARE_SIZE <= pos[0] <= (cell_x + 1) * SQUARE_SIZE and \
                    cell_y * SQUARE_SIZE <= pos[1] <= (cell_y + 1) * SQUARE_SIZE:
                print(
                    f"Checking cell: {cell}, Cell coords: {(cell_x, cell_y)}, Piece: {piece}")
                return piece

        return None

    def get_cell_coords(self, cell_name):
        column_map = {"a": 0, "b": 1, "c": 2}

        column_letter = cell_name[0]
        # We subtract 1 to start the index from 0
        row_number = int(cell_name[1]) - 1

        return column_map[column_letter], row_number

    def select_piece(self, pos):
        """根據給定的位置選擇一個棋子"""
        piece = self.get_piece_at_pos(pos)
        print(f"Piece at pos: {self.get_piece_at_pos(pos)}, Pos: {pos}")
        if piece:
            self.selected_piece = piece
            self.selected_piece_origin = self.get_piece_origin(piece)
            # Store the removed piece and its origin
            self.temp_removed_piece = (
                self.selected_piece, self.selected_piece_origin)
            self.remove_piece_from_origin()  # Immediately remove the piece from its origin
            self.mouse_pos = pos  # Update the mouse position when a piece is selected
            print(
                f"Piece selected: {self.selected_piece}, Origin: {self.selected_piece_origin}")

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

    def place_piece(self, pos):
        if self.setup_mode and self.selected_piece:
            new_cell_name = self.get_cell_name_from_pos(pos)
            print(
                f"New cell name: {new_cell_name}, Selected piece: {self.selected_piece}")
            if new_cell_name:
                self.board_config[new_cell_name] = self.selected_piece
                # Reset the temp removed piece as the placement was successful
                self.temp_removed_piece = None
            else:
                # If the new position is not valid, put back the piece to its origin
                piece, origin = self.temp_removed_piece
                print(f"Piece: {piece}, Origin: {origin}")
                if isinstance(origin, tuple):
                    # If the origin is in the storage area
                    if origin[0] == 'storage1':
                        self.storage_area_player1.insert(origin[1], piece)
                    else:
                        self.storage_area_player2.insert(origin[1], piece)
                else:
                    # If the origin is on the board
                    self.board_config[origin] = piece
            self.selected_piece = None
            # Reset the mouse position when a piece is placed
            self.mouse_pos = (0, 0)
            print(f"Piece placed at: {new_cell_name}")

    def get_cell_name_from_pos(self, pos):
        column_map = {0: "a", 1: "b", 2: "c"}

        x, y = pos
        column = (x - GRID_OFFSET_X) // SQUARE_SIZE
        row = (y - GRID_OFFSET_Y) // SQUARE_SIZE

        if 0 <= column <= 2 and 0 <= row <= 3:
            return column_map[column] + str(row + 1)
        else:
            return None  # 返回 None 如果位置不在有效的棋盤範圍內

    def remove_piece_from_origin(self):
        origin = self.selected_piece_origin

        # Check if the origin is a cell name on the board
        if isinstance(origin, str):
            del self.board_config[origin]
            print(f"Removed piece from cell: {origin}")
        # Check if the origin is an index in the storage areas
        elif isinstance(origin, tuple):
            if origin[0] == 'storage1':
                removed_piece = self.storage_area_player1.pop(origin[1])
                print(f"Removed piece from player 1's storage: {removed_piece}")
            elif origin[0] == 'storage2':
                removed_piece = self.storage_area_player2.pop(origin[1])
                print(f"Removed piece from player 2's storage: {removed_piece}")
