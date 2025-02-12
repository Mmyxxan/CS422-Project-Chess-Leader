import numpy as np

def parse_move(move_str):
    """
    Converts move notation (e.g., 'e2 e4') into board indices.
    """
    try:
        start, end = move_str.split()
        start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])
        return start_row, start_col, end_row, end_col
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

            i, j, r, c = move

            # Validate move
            if not valid[(board_size ** 2) * (board_size * i + j) + board_size * r + c]:
                print("Illegal move. Try again.")
                continue
            else:
                a = (board_size ** 2) * (board_size * i + j) + board_size * r + c
                break

        return a
