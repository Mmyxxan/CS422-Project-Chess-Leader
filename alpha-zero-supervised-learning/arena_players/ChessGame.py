import chess
from .move_index import *

class ChessGame():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        self.board_size = (8, 8)
        self.action_size = 8*8*73

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return chess.Board()

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return self.board_size

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return self.action_size

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        fen = board.fen()
        b = chess.Board(fen=fen)

        move = index_to_move(action, b)
        if not move or move not in b.legal_moves:
            raise ValueError("Invalid or illegal move decoded from action index.")

        b.push(move)
        return b, -player

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        valid = [0] * (64 * 73)
        legal_moves = set(board.legal_moves)  # convert to set for O(1) lookup

        for move in legal_moves:
            index = move_to_index(move)
            if index != -1:  # ignore unsupported/invalid encodings
                valid[index] = 1
            else:
                raise ValueError("ERROR DECODING MOVE")

        return valid

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        if not board.is_game_over():
            return 0

        result = board.result()
        if result == '1-0':
            return 1 if player == 1 else -1
        elif result == '0-1':
            return -1 if player == 1 else 1
        else:
            return 1e-4  # draw

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        if board.turn == chess.WHITE:
            return board.copy()
        else:
            mirrored = board.mirror()
            return mirrored

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.fen()
    
    def display(board):
        files = '  a b c d e f g h'
        print(files)
        print('  -----------------')
        
        for rank in range(7, -1, -1):  # 8 to 1 (from top to bottom)
            row = f"{rank+1}|"
            for file in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                row += f"{piece.symbol() if piece else '.'} "
            print(row + f"|{rank+1}")
        
        print('  -----------------')
        print(files)

