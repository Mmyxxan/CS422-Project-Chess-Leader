import numpy as np
from .ChessPiece import PieceType, MoveDirection73

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
            return None  # Invalid promotion piece
        
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

            dr, dc = r - i, c - j

            if promoted_piece == 'R' or promoted_piece == 'B' or promoted_piece == 'N':
                if dc == 0:
                    base = 64
                elif dc == -1:
                    base = 67
                elif dc == 1:
                    base = 70
                if promoted_piece == 'N':
                    offset = 0
                elif promoted_piece == 'B':
                    offset = 1
                elif promoted_piece == 'R':
                    offset = 2
                index = base + offset
            else:
                index = MoveDirection73.index(dr, dc)

            # print(index)

            # Validate move
            if not valid[(board_size * i + j) * 73 + index]:
                print("Illegal move. Try again.")
                continue
            else:
                a = (board_size * i + j) * 73 + index
                break

        return a
