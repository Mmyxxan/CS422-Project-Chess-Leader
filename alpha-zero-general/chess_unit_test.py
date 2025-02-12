import unittest
from chess import Board, PieceColor, GameState
from chess_test import parse_move

class TestChessGame(unittest.TestCase):
    def setUp(self):
        """Reset the board state before each test."""
        self.board = Board()
        self.current_turn = PieceColor.WHITE  # White always starts

    def test_long_gameplay(self):
        """Tests a longer sequence of legal moves covering all key rules."""
        moves = [
            ("e2", "e4", True, False),  # White Pawn move
            ("e7", "e5", True, False),  # Black Pawn move
            ("b1", "c3", True, False),  # White Knight move
            ("d7", "d6", True, False),  # Black Pawn move
            ("f1", "c4", True, False),  # White Bishop move
            ("b8", "c6", True, False),  # Black Knight move
            ("g1", "f3", True, False),  # White Knight move
            ("c8", "g4", True, False),  # Black Bishop move
            ("h2", "h3", True, False),  # White Pawn move
            ("g4", "f3", True, False),  # Black Bishop captures
            ("d1", "f3", True, False),  # White Queen captures
            ("g8", "f6", True, False),  # Black Knight move
            ("d2", "d3", True, False),  # White Pawn move
            ("c6", "d4", True, False),  # Black Knight move
            ("f3", "d1", True, False),  # White Queen move
            ("h7", "h6", True, False),  # Black Pawn move
            ("c1", "e3", True, False),  # White Bishop move
            ("c7", "c5", True, False),  # Black Pawn move
            ("e1", "g1", True, False),  # White castles kingside
            ("f8", "e7", True, False),  # Black Bishop move
            ("f2", "f4", True, False),  # White Pawn move
            ("e8", "g8", True, False),  # Black castles kingside
            ("f4", "e5", True, False),  # White Pawn captures
            ("d6", "e5", True, False),  # Black Pawn captures
            ("e3", "d4", True, False),  # White Bishop captures
            ("e5", "d4", True, False),  # Black Pawn captures
            ("c3", "a4", True, False),  # White Knight move
            ("a7", "a6", True, False),  # Black Pawn move
            ("c4", "d5", True, False),  # White Bishop move
            ("f6", "d5", True, False),  # Black Knight captures
            ("e4", "d5", True, False),  # White Pawn captures
            ("d8", "d5", True, False),  # Black Queen captures
            ("a4", "b6", True, False),  # White Knight move
            ("d5", "d8", True, False),  # Black Queen move
            ("b6", "a8", True, False),  # White Knight captures
            ("d8", "a8", True, False),  # Black Queen captures
            ("d1", "h5", True, False),  # White Queen move
            ("e7", "g5", True, False),  # Black Bishop move
            ("a1", "e1", True, False),  # White Rook move
            ("g5", "e3", True, True),  # Black Bishop check
            ("g1", "h1", True, False),  # White King move
            ("b7", "b5", True, False),  # Black Pawn move
            ("h5", "c5", True, False),  # White Queen captures
            ("a8", "c8", True, False),  # Black Queen move
            ("f1", "f5", True, False),  # White Rook move
            ("g7", "g6", True, False),  # Black Pawn move
            ("f5", "d5", True, False),  # White Rook move
            ("g8", "g7", True, False),  # Black King move
            ("c2", "c3", True, False),  # White Pawn move
            ("f8", "d8", True, False),  # Black Rook move
            ("c3", "d4", True, False),  # White Pawn captures
            ("c8", "c5", True, False),  # Black Queen captures
            ("d5", "c5", True, False),  # White Rook captures
            ("e3", "d4", True, False),  # Black Bishop captures
            ("c5", "c2", True, False),  # White Rook move
            ("d4", "f6", True, False),  # Black Bishop move
            ("e1", "d1", True, False),  # White Rook move
            ("d8", "d5", True, False),  # Black Rook move
            ("b2", "b3", True, False),  # White Pawn move
            ("a6", "a5", True, False),  # Black Pawn move
            ("g2", "g3", True, False),  # White Pawn move
            ("b5", "b4", True, False),  # Black Pawn move
            ("h1", "g2", True, False),  # White King move
            ("f6", "c3", True, False),  # Black Bishop move
            ("c2", "e2", True, False),  # White Rook move
            ("g6", "g5", True, False),  # Black Pawn move
            ("g2", "f3", True, False),  # White King move
            ("g7", "g6", True, False),  # Black King move
            ("e2", "e4", True, False),  # White Rook move
            ("f7", "f6", True, False),  # Black Pawn move
            ("h3", "h4", True, False),  # White Pawn move
            ("d5", "f5", True, True),  # Black Rook check
            ("f3", "g2", True, False),  # White King move
            ("f5", "d5", True, False),  # Black Rook move
            ("g2", "f3", True, False),  # White King move
            ("d5", "f5", True, True),  # Black Rook check
            ("f3", "e3", True, False),  # White King move
            ("g5", "g4", True, False),  # Black Pawn move
            ("e3", "e2", True, False),  # White King move
            ("h6", "h5", True, False),  # Black Pawn move
            ("d3", "d4", True, False),  # White Pawn move
            ("f5", "d5", True, False),  # Black Rook move
            ("e2", "d3", True, False),  # White King move
            ("g6", "f5", True, False),  # Black King move
            ("d1", "f1", True, True),  # White Rook check
            ("f5", "g6", True, False),  # Black King move
            ("d3", "c4", True, False),  # White King move
            ("d5", "d8", True, False),  # Black Rook move
            ("d4", "d5", True, False),  # White Pawn move
            ("f6", "f5", True, False),  # Black Pawn move
            ("e4", "e6", True, True),  # White Rook check
            ("g6", "f7", True, False),  # Black King move
        ]

        for start, end, valid, checkmate in moves:
            move = parse_move(f"{start} {end}")
            if move is None:
                print(f"Error: Move {start} to {end} could not be parsed.")
                self.board.print_board()
                self.fail(f"Move {start} {end} should be parsed correctly")

            start_row, start_col, end_row, end_col = move
            piece = self.board[start_row][start_col]

            if piece is None:
                print(f"Error: No piece at {start}.")
                self.board.print_board()
                self.fail(f"Piece must exist at {start}")

            if piece.color != self.current_turn:
                print(f"Error: Wrong turn for move {start} to {end}.")
                self.board.print_board()
                self.fail(f"Wrong turn for move {start} {end}")

            valid_moves = piece.get_valid_moves(self.board.board, self.board.last_move)
            valid_move = not not valid_moves[end_row][end_col]
            if valid_move != valid:
                print(f"Error: Move {start} to {end} is {valid_move}, expected {valid}.")
                self.board.print_board()
                self.fail(f"Move {start} {end} should be {valid}")
                
            # Execute move
            self.board.execute_move(piece, end_row, end_col)
            
            # Check if the game is checkmate
            if checkmate == True and self.board.state[0] != GameState.CHECK:
                print("Error: Game is not checkmate.")
                self.board.print_board()
                self.fail(f"Game should be checkmate, move {start} {end}")
                break
            elif checkmate == False and self.board.state[0] == GameState.CHECK:
                print("Error: Game is checkmate.")
                self.board.print_board()
                self.fail(f"Game should not be checkmate, move {start} {end}")
                break

            # Switch turn
            self.current_turn = PieceColor.BLACK if self.current_turn == PieceColor.WHITE else PieceColor.WHITE  
        # Check if the turn is white
        self.assertEqual(self.current_turn, PieceColor.WHITE)
        
        # Print the board before asserting the checkmate
        print("\nFinal Board State:")
        self.board.print_board()

if __name__ == "__main__":
    unittest.main()
