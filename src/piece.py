
import pygame
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y


class Piece:
    def __init__(self, direction):
        self.direction = direction  # Direction can be 'up' or 'down'

    def draw(self, window, row, col):
        # Load the image file for the piece
        piece_image = pygame.image.load(self.image)
        # Scale the image to fit within a square
        piece_image = pygame.transform.scale(
            piece_image, (SQUARE_SIZE, SQUARE_SIZE))
        # Calculate the x, y position of the top left corner of the square where the piece will be drawn
        x = GRID_OFFSET_X + col * SQUARE_SIZE
        y = GRID_OFFSET_Y + row * SQUARE_SIZE
        window.blit(piece_image, (x, y))  # Draw the piece on the board

    def get_available_moves(self, board):
        # This method should be implemented by the subclasses to provide the available moves for a piece
        pass


class Elephant(Piece):
    def __init__(self, direction):
        super().__init__(direction)
        self.image = f"assets/elephant_{direction}.png"

    def get_available_moves(self, board):
        # Define the available moves for the elephant
        if self.direction == 'up':
            return [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]]


class Giraffe(Piece):
    def __init__(self, direction):
        super().__init__(direction)
        self.image = f"assets/giraffe_{direction}.png"

    def get_available_moves(self, board):
        # Define the available moves for the giraffe
        if self.direction == 'up':
            return [(0, 1), (1, 0), (0, -1), (-1, 0)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]]


class Lion(Piece):
    def __init__(self, direction):
        super().__init__(direction)
        self.image = f"assets/lion_{direction}.png"

    def get_available_moves(self, board):
        # Define the available moves for the lion
        if self.direction == 'up':
            return [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]]


class Chick(Piece):
    def __init__(self, direction):
        super().__init__(direction)
        self.image = f"assets/chick_{direction}.png"

    def get_available_moves(self, board):
        # Define the available moves for the chick
        if self.direction == 'up':
            return [(0, -1)]
        else:
            # Flip the move for the down direction
            return [(0, 1)]


class Hen(Piece):
    def __init__(self, direction):
        super().__init__(direction)
        self.image = f"assets/chicken_{direction}.png"

    def get_available_moves(self, board):
        # Define the available moves for the hen
        if self.direction == 'up':
            return [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1)]]
