
import pygame
from const import SQUARE_SIZE, GRID_OFFSET_X, GRID_OFFSET_Y


class Piece:
    image_file = ""  # This will be overridden in each subclass

    def __init__(self, direction):
        self.direction = direction  # Direction can be 'up' or 'down'
        self.image = pygame.image.load(
            f"assets/{self.image_file}_{direction}.png")  # Load the image here

    def draw(self, window, row, col):
        # Scale the image to fit the square size
        scaled_image = pygame.transform.scale(
            self.image, (SQUARE_SIZE, SQUARE_SIZE))
        x = GRID_OFFSET_X + col * SQUARE_SIZE
        y = GRID_OFFSET_Y + row * SQUARE_SIZE
        window.blit(scaled_image, (x, y))

    def get_available_moves(self, board):
        # This method should be implemented by the subclasses to provide the available moves for a piece
        pass


class Elephant(Piece):
    image_file = "elephant"  # Setting the image file name for the Elephant class

    def __init__(self, direction):
        super().__init__(direction)

    def get_available_moves(self, board):
        # Define the available moves for the elephant
        if self.direction == 'up':
            return [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(1, 1), (-1, 1), (1, -1), (-1, -1)]]


class Giraffe(Piece):
    image_file = "giraffe"

    def __init__(self, direction):
        super().__init__(direction)

    def get_available_moves(self, board):
        # Define the available moves for the giraffe
        if self.direction == 'up':
            return [(0, 1), (1, 0), (0, -1), (-1, 0)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]]


class Lion(Piece):
    image_file = "lion"

    def __init__(self, direction):
        super().__init__(direction)

    def get_available_moves(self, board):
        # Define the available moves for the lion
        if self.direction == 'up':
            return [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]]


class Chick(Piece):
    image_file = "chick"

    def __init__(self, direction):
        super().__init__(direction)

    def get_available_moves(self, board):
        # Define the available moves for the chick
        if self.direction == 'up':
            return [(0, -1)]
        else:
            # Flip the move for the down direction
            return [(0, 1)]


class Hen(Piece):
    image_file = "chicken"

    def __init__(self, direction):
        super().__init__(direction)

    def get_available_moves(self, board):
        # Define the available moves for the hen
        if self.direction == 'up':
            return [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1)]
        else:
            # Flip the moves for the down direction
            return [(-x, -y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, 1), (1, 1)]]
