from ..ChessPiece import ChessPiece
from ..ChessPiece import PieceColor
from ..ChessPiece import PieceType

class Bishop(ChessPiece):
    def __init__(self, color=PieceColor.NONE, row=-1, column=-1):
        super().__init__(PieceType.BISHOP, color, row, column)
        
        # The Bishop moves diagonally
        self.move_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  

    def get_valid_moves(self, board, last_move=None):
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        # The bishop moves in four diagonal directions
        for move_direction in self.move_directions:
            for i in range(1, size):  # Move step-by-step
                new_row, new_col = self.row + move_direction[0] * i, self.column + move_direction[1] * i
                if 0 <= new_row < size and 0 <= new_col < size:
                    target_piece = board[new_row][new_col]

                    if target_piece.piece_type == PieceType.NONE:  # Empty square
                        if super().is_legal_move(board, new_row, new_col):
                            matrix[new_row][new_col] = 1  
                    elif target_piece.color != self.color:  # Enemy piece -> Can capture
                        if super().is_legal_move(board, new_row, new_col):
                            matrix[new_row][new_col] = 1  
                        break  # Stop moving after capturing
                    else:  # Friendly piece -> Blocked
                        break

        return matrix  # Return the move matrix
    
    def get_valid_moves_without_check(self, board, last_move=None):
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        # The bishop moves in four diagonal directions
        for move_direction in self.move_directions:
            for i in range(1, size):  # Move step-by-step
                new_row, new_col = self.row + move_direction[0] * i, self.column + move_direction[1] * i
                if 0 <= new_row < size and 0 <= new_col < size:
                    target_piece = board[new_row][new_col]

                    if target_piece.piece_type == PieceType.NONE:  # Empty square
                        matrix[new_row][new_col] = 1  
                    elif target_piece.color != self.color:  # Enemy piece -> Can capture
                        matrix[new_row][new_col] = 1  
                        break  # Stop moving after capturing
                    else:  # Friendly piece -> Blocked
                        break

        return matrix  # Return the move matrix
