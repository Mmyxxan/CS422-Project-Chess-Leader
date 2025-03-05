from ..ChessPiece import ChessPiece
from ..ChessPiece import PieceColor
from ..ChessPiece import PieceType
from .Rook import Rook
from .Knight import Knight
from .Bishop import Bishop
from .Queen import Queen

class Pawn(ChessPiece):
    def __init__(self, color=PieceColor.NONE, row=-1, column=-1):
        super().__init__(PieceType.PAWN, color, row, column)
        
        # Adjust move directions based on color
        self.direction = -1 if color == PieceColor.WHITE else 1
        self.move_directions = [(self.direction, 0)]  # Normal move
        if (self.color == PieceColor.WHITE and self.row == 6) or (self.color == PieceColor.BLACK and self.row == 1):
            self.move_directions.append((2 * self.direction, 0))  # Two-square move
        
        self.attack_directions = [(self.direction, 1), (self.direction, -1)]  # Diagonal attack moves
        # self.en_passant_target = None

    def get_valid_moves_without_check(self, board, last_move=None):
        matrix = [[0 for _ in range(len(board))] for _ in range(len(board))]

        # Check normal movement (can only move forward if the cell is empty)
        for move_direction in self.move_directions:
            new_row, new_col = self.row + move_direction[0], self.column + move_direction[1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board):
                if board[new_row][new_col].piece_type == PieceType.NONE:  # Empty square
                    matrix[new_row][new_col] = 1
                else:
                    break  # If there's a piece in front, stop further movement

        # Check attack moves (can only attack diagonally if an opponent piece exists)
        for attack_direction in self.attack_directions:
            new_row, new_col = self.row + attack_direction[0], self.column + attack_direction[1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board):
                target_piece = board[new_row][new_col]
                if target_piece.piece_type != PieceType.NONE and target_piece.color != self.color:
                    matrix[new_row][new_col] = 1  # Can capture

        # Check for en passant
        if last_move:
            last_piece, last_from, last_to = last_move
            if (
                isinstance(last_piece, Pawn)
                and last_piece.color != self.color
                and abs(last_from[0] - last_to[0]) == 2  # Was a two-step pawn move
                and last_from[1] in [self.column - 1, self.column + 1]  # Was adjacent to this pawn
                and self.row == last_to[0]  # En passant can only occur if on the same rank
            ):
                matrix[last_from[0] - self.direction][last_from[1]] = 1  # En passant capture square

        # if self.en_passant_target:
        #     en_passant_row, en_passant_column = self.en_passant_target
        #     if (en_passant_column == self.column + 1):
        #         matrix[self.row + self.direction][self.column + 1] = 1
        #     elif (en_passant_column == self.column - 1):
        #         matrix[self.row + self.direction][self.column - 1] = 1

        return matrix  # Return the move matrix

    def get_valid_moves(self, board, last_move=None):
        matrix = [[0 for _ in range(len(board))] for _ in range(len(board))]

        # Check normal movement (can only move forward if the cell is empty)
        for move_direction in self.move_directions:
            new_row, new_col = self.row + move_direction[0], self.column + move_direction[1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board):
                if board[new_row][new_col].piece_type == PieceType.NONE:  # Empty square
                    if super().is_legal_move(board, new_row, new_col):
                        matrix[new_row][new_col] = 1
                else:
                    break  # If there's a piece in front, stop further movement

        # Check attack moves (can only attack diagonally if an opponent piece exists)
        for attack_direction in self.attack_directions:
            new_row, new_col = self.row + attack_direction[0], self.column + attack_direction[1]
            if 0 <= new_row < len(board) and 0 <= new_col < len(board):
                target_piece = board[new_row][new_col]
                if target_piece.piece_type != PieceType.NONE and target_piece.color != self.color:
                    if super().is_legal_move(board, new_row, new_col):
                        matrix[new_row][new_col] = 1  # Can capture

        # Check for en passant
        if last_move:
            last_piece, last_from, last_to = last_move
            if (
                isinstance(last_piece, Pawn)
                and last_piece.color != self.color
                and abs(last_from[0] - last_to[0]) == 2  # Was a two-step pawn move
                and last_from[1] in [self.column - 1, self.column + 1]  # Was adjacent to this pawn
                and self.row == last_to[0]  # En passant can only occur if on the same rank
            ):
                if super().is_legal_move(board, last_from[0] - self.direction, last_from[1]):
                    matrix[last_from[0] - self.direction][last_from[1]] = 1  # En passant capture square

        # if self.en_passant_target:
        #     en_passant_row, en_passant_column = self.en_passant_target
        #     if (en_passant_column == self.column + 1):
        #         matrix[self.row + self.direction][self.column + 1] = 1
        #     elif (en_passant_column == self.column - 1):
        #         matrix[self.row + self.direction][self.column - 1] = 1

        return matrix  # Return the move matrix

    def execute_move(self, board, new_row, new_col, last_move=None, promoted_piece=PieceType.QUEEN):
        """
        Move the pawn to (new_row, new_col) and update its state.
        """
        # if new_col != self.column and board[new_row][new_col].piece_type == PieceType.NONE:
        #     self.en_passant_target = None
        #     if new_col == self.column + 1:
        #         if 0 <= self.column + 2 < len(board) and isinstance(board[self.row][self.column + 2], Pawn) and board[self.row][self.column + 2].color == self.color:
        #             board[self.row][self.column + 2].en_passant_target = None
        #     elif new_col == self.column - 1:
        #         if 0 <= self.column - 2 < len(board) and isinstance(board[self.row][self.column - 2], Pawn) and board[self.row][self.column - 2].color == self.color:
        #             board[self.row][self.column - 2].en_passant_target = None

        # Remove en passant caught pawn
        if new_col != self.column and board[new_row][new_col].piece_type == PieceType.NONE:
            board[new_row][new_col].die()
            board[new_row - self.direction][new_col].die()
            target_piece = board[new_row - self.direction][new_col]
            board[new_row - self.direction][new_col] = ChessPiece()
            board[new_row][new_col] = self
            board[self.row][self.column] = ChessPiece()
            self.row = new_row
            self.column = new_col
        #
        elif board[new_row][new_col].piece_type == PieceType.NONE or board[new_row][new_col].color != self.color:
            # Kill the target piece 
            board[new_row][new_col].die()
            target_piece = board[new_row - self.direction][new_col]
            # Move the piece
            board[self.row][self.column] = ChessPiece()  # Clear old position
            # if abs(new_row - self.row) == 2:
            #     if 0 <= new_col + 1 < len(board) and isinstance(board[new_row][new_col + 1], Pawn) and board[new_row][new_col + 1].color != self.color:
            #         board[new_row][new_col + 1].en_passant_target = (new_row, new_col)
            #     if 0 <= new_col - 1 < len(board) and isinstance(board[new_row][new_col - 1], Pawn) and board[new_row][new_col - 1].color != self.color:
            #         board[new_row][new_col - 1].en_passant_target = (new_row, new_col)
            self.row, self.column = new_row, new_col
            board[new_row][new_col] = self  # Place pawn in new position

            # After the first move, pawns cannot move by 2 steps
            self.move_directions = [(self.direction, 0)]  # Normal move
            self.has_moved = True

        # Promote when come to the other side of the board
        if (self.color == PieceColor.WHITE and self.row == 0) or (self.color == PieceColor.BLACK and self.row == 7):
            self.promote(board, promoted_piece)

        return board, target_piece if target_piece.piece_type != PieceType.NONE else None

    def promote(self, board, new_type):
        """
        If a pawn reaches the opposite side of the board, it is promoted to a higher piece (except king). 
        There is no limit to how many pawns can be promoted.
        """
        if new_type == PieceType.KING:
            raise ValueError("Pawns cannot be promoted to a King!")

        if (self.color == PieceColor.WHITE and self.row == 0) or (self.color == PieceColor.BLACK and self.row == 7):
            # Determine the new piece
            if new_type == PieceType.QUEEN:
                # self.piece_type = PieceType.QUEEN
                promoted_piece = Queen(self.color)
            elif new_type == PieceType.ROOK:
                # self.piece_type = PieceType.ROOK
                promoted_piece = Rook(self.color)
            elif new_type == PieceType.BISHOP:
                # self.piece_type = PieceType.BISHOP
                promoted_piece = Bishop(self.color)
            elif new_type == PieceType.KNIGHT:
                # self.piece_type = PieceType.KNIGHT
                promoted_piece = Knight(self.color)
            else:
                raise ValueError("Invalid promotion piece type!")

            # Place the promoted piece on the board
            promoted_piece.has_moved = True
            promoted_piece.place_piece(board, self.row, self.column) 
            
        else:
            raise ValueError("Pawn cannot be promoted unless it reaches the last rank!")
        
    def is_promotable(self, new_row):
        # return True if (self.color == PieceColor.WHITE and new_row == 0) or (self.color == PieceColor.BLACK and new_row == 7) else False
        return True if new_row == 0 or new_row == 7 else False
    
    # def reverse_color(self):
    #     if self.color == PieceColor.WHITE:
    #         self.color = PieceColor.BLACK
    #     else:
    #         self.color = PieceColor.WHITE
    #     self.direction = -self.direction
