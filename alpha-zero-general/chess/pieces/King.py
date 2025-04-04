from ..ChessPiece import ChessPiece
from ..ChessPiece import PieceColor
from ..ChessPiece import PieceType, MoveDirection73
from .Rook import Rook
from enum import Enum

class CastlingSide(Enum):
    QUEEN_SIDE = 0
    KING_SIDE = 1

class King(ChessPiece):
    def __init__(self, color=PieceColor.NONE, row=-1, column=-1):
        super().__init__(PieceType.KING, color, row, column)
        
        # The King moves one step in all 8 directions
        # self.move_directions = [
        #     (1, 1), (1, 0), (1, -1),  # Down-Right, Down, Down-Left
        #     (0, 1), (0, -1),          # Right, Left
        #     (-1, 1), (-1, 0), (-1, -1)  # Up-Right, Up, Up-Left
        # ]

    def can_castle(self, board, side):
        if not self.has_moved:  # King must not have moved before
            if side == CastlingSide.KING_SIDE:
                # Kingside castling
                if isinstance(board[self.row][self.column + 3], Rook) and not board[self.row][self.column + 3].has_moved:
                    if board[self.row][self.column + 1].piece_type == PieceType.NONE and board[self.row][self.column + 2].piece_type == PieceType.NONE:
                        for i in range(3):
                            if not super().is_legal_move(board, self.row, self.column + i):
                                return False
                        return True
                    
            elif side == CastlingSide.QUEEN_SIDE:
                # Queenside castling
                if isinstance(board[self.row][self.column - 4], Rook) and not board[self.row][self.column - 4].has_moved:
                    if (board[self.row][self.column - 1].piece_type == PieceType.NONE and 
                        board[self.row][self.column - 2].piece_type == PieceType.NONE and 
                        board[self.row][self.column - 3].piece_type == PieceType.NONE):
                        for i in range(3):
                            if not super().is_legal_move(board, self.row, self.column - i):
                                return False
                        return True
                    
        return False

    def get_valid_moves(self, board, last_move=None):
        size = len(board)
        mask = [0] * 73

        # Normal 1-step moves (first 8 sliding directions)
        for i in range(0, 56, 7):
            dr, dc = MoveDirection73.get(i)
            new_row = self.row + dr
            new_col = self.column + dc

            if 0 <= new_row < size and 0 <= new_col < size:
                target = board[new_row][new_col]
                if target.piece_type == PieceType.NONE or target.color != self.color:
                    if super().is_legal_move(board, new_row, new_col):
                        mask[i] = 1

        # Castling - Kingside (index 71)
        if not self.has_moved:
            try:
                rook = board[self.row][self.column + 3]
                if isinstance(rook, Rook) and not rook.has_moved:
                    if (board[self.row][self.column + 1].piece_type == PieceType.NONE and
                        board[self.row][self.column + 2].piece_type == PieceType.NONE):
                        path_safe = True
                        for i in range(3):
                            if not super().is_legal_move(board, self.row, self.column + i):
                                path_safe = False
                                break
                        if path_safe:
                            mask[15] = 1
            except IndexError:
                pass

            # Castling - Queenside (index 72)
            try:
                rook = board[self.row][self.column - 4]
                if isinstance(rook, Rook) and not rook.has_moved:
                    if (board[self.row][self.column - 1].piece_type == PieceType.NONE and
                        board[self.row][self.column - 2].piece_type == PieceType.NONE and
                        board[self.row][self.column - 3].piece_type == PieceType.NONE):
                        path_safe = True
                        for i in range(3):
                            if not super().is_legal_move(board, self.row, self.column - i):
                                path_safe = False
                                break
                        if path_safe:
                            mask[22] = 1
            except IndexError:
                pass

        return mask
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        # Normal one-step moves
        for move_direction in self.move_directions:
            new_row, new_col = self.row + move_direction[0], self.column + move_direction[1]
            if 0 <= new_row < size and 0 <= new_col < size:
                target_piece = board[new_row][new_col]
                if target_piece.piece_type == PieceType.NONE or target_piece.color != self.color:
                    if super().is_legal_move(board, new_row, new_col):
                        matrix[new_row][new_col] = 1  # Empty or enemy piece (can capture)

        # Castling move
        # The king is not in check.
        # The king does not move through or into check.
        if not self.has_moved:  # King must not have moved before
            # Kingside castling
            if isinstance(board[self.row][self.column + 3], Rook) and not board[self.row][self.column + 3].has_moved:
                if board[self.row][self.column + 1].piece_type == PieceType.NONE and board[self.row][self.column + 2].piece_type == PieceType.NONE:
                    matrix[self.row][self.column + 2] = 1  # Castling is valid
                    for i in range(3):
                        if not super().is_legal_move(board, self.row, self.column + i):
                            matrix[self.row][self.column + 2] = 0
                            break

            # Queenside castling
            if isinstance(board[self.row][self.column - 4], Rook) and not board[self.row][self.column - 4].has_moved:
                if (board[self.row][self.column - 1].piece_type == PieceType.NONE and 
                    board[self.row][self.column - 2].piece_type == PieceType.NONE and 
                    board[self.row][self.column - 3].piece_type == PieceType.NONE):
                    matrix[self.row][self.column - 2] = 1  # Castling is valid
                    for i in range(3):
                        if not super().is_legal_move(board, self.row, self.column - i):
                            matrix[self.row][self.column - 2] = 0
                            break

        return matrix  # Return the move matrix

    def execute_move(self, board, new_row, new_col, last_move=None, promoted_piece=PieceType.QUEEN):
        """
        Move the King to (new_row, new_col) and update its state.
        Handles normal moves and castling.
        NOTE: This version is lack of dead pieces logic
        """
        if abs(new_col - self.column) == 2:  # Castling move
            if new_col > self.column:  # Kingside castling
                rook_col = self.column + 3
                new_rook_col = self.column + 1
            else:  # Queenside castling
                rook_col = self.column - 4
                new_rook_col = self.column - 1

            # Move the rook
            rook = board[self.row][rook_col]
            # board[self.row][rook_col] = ChessPiece()  # Clear old rook position
            ChessPiece().place_piece(board, self.row, rook_col)
            board[self.row][new_rook_col].die()
            board[self.row][new_rook_col] = rook  # Place rook in new position
            rook.column = new_rook_col

        # Normal move execution
        target_piece = board[new_row][new_col]
        if target_piece.piece_type == PieceType.NONE or target_piece.color != self.color:
            target_piece.die()  # Capture the piece if it's an enemy
            # board[self.row][self.column] = ChessPiece()  # Clear old position
            ChessPiece().place_piece(board, self.row, self.column)
            self.row, self.column = new_row, new_col
            board[new_row][new_col] = self  # Place King in new position

        # Mark King as moved (castling is no longer possible)
        self.has_moved = True

        return board, target_piece if target_piece.piece_type != PieceType.NONE else None
    
    def get_valid_moves_without_check(self, board, last_move=None):
        return self.get_action_mask(board, last_move)
        size = len(board)
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        # Normal one-step moves
        for move_direction in self.move_directions:
            new_row, new_col = self.row + move_direction[0], self.column + move_direction[1]
            if 0 <= new_row < size and 0 <= new_col < size:
                target_piece = board[new_row][new_col]
                if target_piece.piece_type == PieceType.NONE or target_piece.color != self.color:
                    matrix[new_row][new_col] = 1  # Empty or enemy piece (can capture)

        # Castling move
        # The king is not in check.
        # The king does not move through or into check.
        if not self.has_moved:  # King must not have moved before
            # Kingside castling
            if isinstance(board[self.row][self.column + 3], Rook) and not board[self.row][self.column + 3].has_moved:
                if board[self.row][self.column + 1].piece_type == PieceType.NONE and board[self.row][self.column + 2].piece_type == PieceType.NONE:
                    matrix[self.row][self.column + 2] = 1  # Castling is valid
                    for i in range(3):
                        if not super().is_legal_move_for_castling(board, self.row, self.column + i):
                            matrix[self.row][self.column + 2] = 0
                            break

            # Queenside castling
            if isinstance(board[self.row][self.column - 4], Rook) and not board[self.row][self.column - 4].has_moved:
                if (board[self.row][self.column - 1].piece_type == PieceType.NONE and 
                    board[self.row][self.column - 2].piece_type == PieceType.NONE and 
                    board[self.row][self.column - 3].piece_type == PieceType.NONE):
                    matrix[self.row][self.column - 2] = 1  # Castling is valid
                    for i in range(3):
                        if not super().is_legal_move_for_castling(board, self.row, self.column - i):
                            matrix[self.row][self.column - 2] = 0
                            break

        return matrix  # Return the move matrix
    
    def get_action_mask(self, board, last_move=None):
        size = len(board)
        mask = [0] * 73

        # Normal 1-step moves (first 8 sliding directions)
        for i in range(0, 56, 7):
            dr, dc = MoveDirection73.get(i)
            # if abs(dr) > 1 or abs(dc) > 1:
            #     print("FALSE")
            new_row = self.row + dr
            new_col = self.column + dc

            if 0 <= new_row < size and 0 <= new_col < size:
                target = board[new_row][new_col]
                if target.piece_type == PieceType.NONE or target.color != self.color:
                    mask[i] = 1

        # Castling - Kingside (index 71)
        if not self.has_moved:
            try:
                rook = board[self.row][self.column + 3]
                if isinstance(rook, Rook) and not rook.has_moved:
                    if (board[self.row][self.column + 1].piece_type == PieceType.NONE and
                        board[self.row][self.column + 2].piece_type == PieceType.NONE):
                        path_safe = True
                        for i in range(3):
                            if not super().is_legal_move_for_castling(board, self.row, self.column + i):
                                path_safe = False
                                break
                        if path_safe:
                            mask[15] = 1
            except IndexError:
                pass

            # Castling - Queenside (index 72)
            try:
                rook = board[self.row][self.column - 4]
                if isinstance(rook, Rook) and not rook.has_moved:
                    if (board[self.row][self.column - 1].piece_type == PieceType.NONE and
                        board[self.row][self.column - 2].piece_type == PieceType.NONE and
                        board[self.row][self.column - 3].piece_type == PieceType.NONE):
                        path_safe = True
                        for i in range(3):
                            if not super().is_legal_move_for_castling(board, self.row, self.column - i):
                                path_safe = False
                                break
                        if path_safe:
                            mask[22] = 1
            except IndexError:
                pass

        return mask
