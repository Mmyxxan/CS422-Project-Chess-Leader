from ..ChessPiece import ChessPiece
from ..ChessPiece import PieceColor
from ..ChessPiece import PieceType
from ..ChessPiece import MoveDirection73

class Rook(ChessPiece):
    def __init__(self, color=PieceColor.NONE, row=-1, column=-1):
        super().__init__(PieceType.ROOK, color, row, column)
        
        # The Rook moves in straight lines (vertically & horizontally)
        # self.move_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Up, Down, Right, Left

    def get_valid_moves(self, board, last_move=None):
        mask = self.get_action_mask(board, last_move)
        for i in range(len(mask)):
            dr, dc = MoveDirection73.get(i)
            new_row = self.row + dr
            new_col = self.column + dc
            if mask[i] and not super().is_legal_move(board, new_row, new_col):
                mask[i] = 0
        return mask
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        # The rook moves in four straight directions: up, down, left, right
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
        return self.get_action_mask(board, last_move)
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        # The rook moves in four straight directions: up, down, left, right
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
    
    def get_action_mask(self, board, last_move=None):
        size = len(board)
        mask = [0] * 73

        # Rook uses the first 4 sliding directions: up, down, right, left
        # Each direction has 7 steps → indices 0 to 27
        # Directions:
        # (1,0), (2,0), ..., (7,0)     ↓
        # (-1,0), (-2,0), ..., (-7,0) ↑
        # (0,1), (0,2), ..., (0,7)     →
        # (0,-1), (0,-2), ..., (0,-7)  ←

        for base in range(0, 28, 7):  # 4 directions, each with 7 distances
            for offset in range(7):
                i = base + offset
                dr, dc = MoveDirection73.get(i)
                new_row = self.row + dr
                new_col = self.column + dc

                if not (0 <= new_row < size and 0 <= new_col < size):
                    break  # Out of bounds, stop in this direction

                target = board[new_row][new_col]

                if target.piece_type == PieceType.NONE:
                    mask[i] = 1  # Empty square, rook can move here
                elif target.color != self.color:
                    mask[i] = 1  # Enemy piece, rook can capture
                    break        # But can't go further
                else:
                    break        # Friendly piece blocks the way

        return mask
