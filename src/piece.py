
class Piece:
    def __init__(self, player):
        """
        Initialize a new piece.
        
        :param player: The player who owns this piece ('player1' or 'player2').
        """
        self.player = player

    def get_available_moves(self, board):
        """
        Get a list of available moves for this piece.

        :param board: The current state of the game board.
        :return: A list of available moves.
        """
        raise NotImplementedError("This method should be overridden by subclasses")


class Lion(Piece):
    def get_available_moves(self, board):
        # TODO: Implement the method to get available moves for the Lion piece
        pass


class Elephant(Piece):
    def get_available_moves(self, board):
        # TODO: Implement the method to get available moves for the Elephant piece
        pass


class Giraffe(Piece):
    def get_available_moves(self, board):
        # TODO: Implement the method to get available moves for the Giraffe piece
        pass


class Chick(Piece):
    def get_available_moves(self, board):
        # TODO: Implement the method to get available moves for the Chick piece
        pass


class Chicken(Piece):
    def get_available_moves(self, board):
        # TODO: Implement the method to get available moves for the Chicken piece
        pass
