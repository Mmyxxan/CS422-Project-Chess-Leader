import numpy as np
from .ChessPiece import PieceType

def parse_move(move_str):
    """
    Converts move notation (e.g., 'e2 e4' or 'e7 e8 Q') into board indices.
    Handles optional pawn promotion (e.g., 'e7 e8 Q' -> promotion to Queen).
    """
    try:
        parts = move_str.split()
        if len(parts) < 2 or len(parts) > 3:
            return None  # Invalid format
        
        start, end = parts[0], parts[1]
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        
        promotion = parts[2].upper() if len(parts) == 3 else None
        if promotion and promotion not in {'Q', 'R', 'B', 'N'}:
            return 'P'  # Invalid promotion piece
        
        return start_row, start_col, end_row, end_col, promotion
    except:
        return None

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a

class HumanChessPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        board_size = len(board.board)
        valid = self.game.getValidMoves(board, 1)
        # for action in range(len(valid)):
        #     if valid[action]:
        #         cell = int(action / (board_size ** 2))
        #         move = action % (board_size ** 2)
        #         piece, new_row, new_col = board.board[int(cell / board_size)][cell % board_size], int(move / board_size), move % board_size
        #         print(piece.row, piece.column, piece.piece_type, new_row, new_col)
        while True: 
            # Get user input
            move_str = input(f"Your move (e.g., 'e2 e4'): ").strip().lower()

            move = parse_move(move_str)
            if not move:
                print("Invalid move format. Use notation like 'e2 e4'. Try again.")
                continue

            i, j, r, c, promoted_piece = move

            if promoted_piece == 'P':
                promotion_piece = 0
            elif promoted_piece == 'Q':
                promotion_piece = 4
            elif promoted_piece == 'R':
                promotion_piece = 3
            elif promoted_piece == 'B':
                promotion_piece = 1
            elif promoted_piece == 'N':
                promotion_piece = 2                

            # Validate move
            if not valid[(board_size ** 2) * (board_size * i + j) + board_size * r + c + (8 ** 2) * (8 ** 2) * promotion_piece]:
                print("Illegal move. Try again.")
                continue
            else:
                a = (board_size ** 2) * (board_size * i + j) + board_size * r + c
                break

        return a
