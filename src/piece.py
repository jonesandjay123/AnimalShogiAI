
import pygame

piece_type_map = {
    "L": ("Lion", "lion"),
    "G": ("Giraffe", "giraffe"),
    "E": ("Elephant", "elephant"),
    "C": ("Chick", "chick"),
    "H": ("Chicken", "chicken")
}

class Piece:
    def __init__(self, piece_type, player):
        self.piece_type = piece_type
        self.player = player

        # Set the name and image file name based on the piece type
        self.name, self.image_file_name = piece_type_map[piece_type]

        # Set the direction based on the player
        self.direction = "up" if player == 1 else "down"

        # Load the image based on the image file name and direction
        self.image = pygame.image.load(
            f"assets/{self.image_file_name}_{self.direction}.png")

        # Set the move rules based on the piece type
        self.move_rules = self.get_move_rules()

    def get_move_rules(self):
        # Define the move rules for each piece type
        move_rules = {
            "L": [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)],
            "G": [(0, 1), (0, -1), (1, 0), (-1, 0)],
            "E": [(1, 1), (-1, 1), (1, -1), (-1, -1)],
            "C": [(0, 1) if self.player == 1 else (0, -1)],
            "H": [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        }

        # Get the move rules based on the piece type
        return move_rules[self.piece_type]

    def get_available_moves(self):
        # Get the moves based on the piece type
        if self.direction == "down":
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in self.move_rules]
        return self.move_rules

    def update_position(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def update_player(self, new_player):
        # 更新 player 和 direction 屬性
        self.player = new_player
        self.direction = "up" if new_player == 1 else "down"
        
        # 重新加載正確的圖像
        self.image = pygame.image.load(
            f"assets/{self.image_file_name}_{self.direction}.png")
        
        # 更新移動規則，因為它們也可能依賴於 player 屬性
        self.move_rules = self.get_move_rules()