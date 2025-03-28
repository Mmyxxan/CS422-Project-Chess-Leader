from ..ChessPiece import ChessPiece
from ..ChessPiece import PieceColor
from ..ChessPiece import PieceType, MoveDirection73

class Knight(ChessPiece):
    def __init__(self, color=PieceColor.NONE, row=-1, column=-1):
        super().__init__(PieceType.KNIGHT, color, row, column)
        
        # Knight moves in an "L" shape: (±2, ±1) or (±1, ±2)
        # self.move_directions = [
        #     (2, 1), (2, -1), (-2, 1), (-2, -1),
        #     (1, 2), (1, -2), (-1, 2), (-1, -2)
        # ]

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

        for move_direction in self.move_directions:
            new_row, new_col = self.row + move_direction[0], self.column + move_direction[1]

            if 0 <= new_row < size and 0 <= new_col < size:
                target_piece = board[new_row][new_col]

                # Allow move if the square is empty or occupied by an opponent
                if target_piece.piece_type == PieceType.NONE or target_piece.color != self.color:
                    if super().is_legal_move(board, new_row, new_col):
                        matrix[new_row][new_col] = 1  

        return matrix  # Return the move matrix
    
    def get_valid_moves_without_check(self, board, last_move=None):
        return self.get_action_mask(board, last_move)
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        for move_direction in self.move_directions:
            new_row, new_col = self.row + move_direction[0], self.column + move_direction[1]

            if 0 <= new_row < size and 0 <= new_col < size:
                target_piece = board[new_row][new_col]

                # Allow move if the square is empty or occupied by an opponent
                if target_piece.piece_type == PieceType.NONE or target_piece.color != self.color:
                    matrix[new_row][new_col] = 1  

        return matrix  # Return the move matrix
    
    def get_action_mask(self, board, last_move=None):
        size = len(board)
        mask = [0] * 73

        for i in range(56, 64):  # Knight move directions
            dr, dc = MoveDirection73.get(i)
            new_row, new_col = self.row + dr, self.column + dc

            if not (0 <= new_row < size and 0 <= new_col < size):
                continue

            target = board[new_row][new_col]
            if target.piece_type == PieceType.NONE or target.color != self.color:
                mask[i] = 1

        return mask
