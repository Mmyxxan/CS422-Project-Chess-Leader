from enum import Enum
import copy

class PieceType(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class PieceColor(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2


class MoveDirection73:
    directions = []

    # Sliding directions: 8 directions × 7 distances
    slide_dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
    for dr, dc in slide_dirs:
        for dist in range(1, 8):
            directions.append((dr * dist, dc * dist))

    # Knight moves: 8
    directions.extend([
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ])

    # Underpromotions (N, B, R): 3 × 3 directions (forward, left, right)
    # Forward
    directions.extend([(-1, 0)] * 3)
    # Left capture
    directions.extend([(-1, -1)] * 3)
    # Right capture
    directions.extend([(-1, 1)] * 3)

    # Castling (King-side and Queen-side)
    # directions.append((0, 2))
    # directions.append((0, -2))

    # print(len(directions))

    # for i in range(73):
    #     print(i, directions[i])

    assert len(directions) == 73, "Directions must be exactly 73."
    @classmethod
    def get(self, index: int):
        return self.directions[index]
    # @classmethod
    # def index(self, dr: int, dc: int):
    #     """Returns the first index matching the given delta."""
    #     return self.directions.index((dr, dc))
    @classmethod
    def index(self, dr: int, dc: int) -> int:
        """Returns the index matching the given delta, or -1 if not found."""
        try:
            return self.directions.index((dr, dc))
        except ValueError:
            return -1
    @classmethod
    def all(self):
        return self.directions
    @classmethod
    def get_promotion_indices(self):
        """Returns a list of indices for underpromotion directions."""
        return list(range(64, 73))
    @classmethod
    def get_promotion_piece(self, index):
        """Return the promotion piece"""
        if index == 64 or index == 67 or index == 70:
            return PieceType.KNIGHT
        if index == 65 or index == 68 or index == 71:
            return PieceType.BISHOP
        return PieceType.ROOK
    @classmethod
    def get_knight_indices(self):
        return list(range(56, 64))
    @classmethod
    def get_sliding_indices(self):
        return list(range(0, 56))
    @classmethod
    def get_castling_indices(self):
        return [71, 72]
    @classmethod 
    def translate_move(self, piece, index):
        dr, dc = self.get(index)
        new_row = piece.row + dr
        new_col = piece.column + dc
        promoted_piece = PieceType.QUEEN

        if index in self.get_promotion_indices():
            dr, dc = piece.direction, self.get(index)[1]
            new_row = piece.row + dr
            new_col = piece.column + dc
            promoted_piece = self.get_promotion_piece(index)
        
        return new_row, new_col, promoted_piece

class ChessPiece:
    def __init__(self, piece_type=PieceType.NONE, color=PieceColor.NONE, row=-1, column=-1):
        self.piece_type = piece_type
        self.color = color
        self.row = row
        self.column = column
        # self.is_alive = True
        self.has_moved = False

    # def __deepcopy__(self, memo):
    #     # Only copy the necessary attributes, avoid recursive references
    #     cls = self.__class__
    #     copied = cls.__new__(cls)
    #     memo[id(self)] = copied

    #     # Manually copy the primitive attributes
    #     copied.piece_type = self.piece_type
    #     copied.color = self.color
    #     copied.row = self.row
    #     copied.column = self.column
    #     copied.is_alive = self.is_alive
    #     copied.has_moved = self.has_moved

    #     return copied

    def __str__(self):
        piece_symbols = {
            (PieceType.PAWN, PieceColor.WHITE): "P",
            (PieceType.PAWN, PieceColor.BLACK): "p",
            (PieceType.KNIGHT, PieceColor.WHITE): "N",
            (PieceType.KNIGHT, PieceColor.BLACK): "n",
            (PieceType.BISHOP, PieceColor.WHITE): "B",
            (PieceType.BISHOP, PieceColor.BLACK): "b",
            (PieceType.ROOK, PieceColor.WHITE): "R",
            (PieceType.ROOK, PieceColor.BLACK): "r",
            (PieceType.QUEEN, PieceColor.WHITE): "Q",
            (PieceType.QUEEN, PieceColor.BLACK): "q",
            (PieceType.KING, PieceColor.WHITE): "K",
            (PieceType.KING, PieceColor.BLACK): "k",
            (PieceType.NONE, PieceColor.NONE): "."
        }
        return piece_symbols[(self.piece_type, self.color)]
    
    def find_king(self, board, color):
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j].piece_type == PieceType.KING and board[i][j].color == color:
                    return board[i][j]
        print()
        for row in board:
            print(" ".join(str(piece) for piece in row))
        return None
    
    def is_king_in_check_for_castling(self, board, king, last_move=None):
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j].piece_type != PieceType.KING and board[i][j].piece_type != PieceType.NONE and board[i][j].color != king.color:
                    mask = board[i][j].get_valid_moves_without_check(board, last_move)
                    dr, dc = king.row - board[i][j].row, king.column - board[i][j].column
                    action = MoveDirection73.index(dr, dc)
                    if action != -1 and mask[action]:
                        return True
                    # for index in range(len(mask)):
                    #     if mask[index]:
                    #         move = MoveDirection73.translate_move(board[i][j], index)
                    #         if move[0] == king.row and move[1] == king.column:
                    #             return True
                elif board[i][j].piece_type == PieceType.KING and board[i][j].color != king.color:
                    opponent_king = board[i][j]
                    if opponent_king.has_moved:
                        mask = opponent_king.get_valid_moves_without_check(board, last_move)
                        dr, dc = king.row - opponent_king.row, king.column - opponent_king.column
                        action = MoveDirection73.index(dr, dc)
                        if action != -1 and mask[action]:
                            return True
                        # for index in range(len(mask)):
                        #     if mask[index]:
                        #         move = MoveDirection73.translate_move(opponent_king, index)
                        #         if move[0] == king.row and move[1] == king.column:
                        #             return True
        return False
                
    def is_king_in_check(self, board, king, last_move=None):
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j].piece_type != PieceType.NONE and board[i][j].color != king.color:
                    mask = board[i][j].get_valid_moves_without_check(board, last_move)
                    dr, dc = king.row - board[i][j].row, king.column - board[i][j].column
                    action = MoveDirection73.index(dr, dc)
                    if action != -1 and mask[action]:
                        return True
                    # for index in range(len(mask)):
                    #     if mask[index]:
                    #         move = MoveDirection73.translate_move(board[i][j], index)
                    #         if move[0] == king.row and move[1] == king.column:
                    #             return True
        return False
    
    def is_legal_move_for_castling(self, board, new_row, new_col):
        """
        Checks if moving the piece to (new_row, new_col) is legal.
        A move is illegal if it puts the player's king in check.
        """
        # Create a deep copy of the board to simulate the move
        simulated_board = copy.deepcopy(board)

        # Find this piece in the copied board
        simulated_piece = simulated_board[self.row][self.column]
        # target_piece = simulated_board[new_row][new_col]

        # Record last_move
        last_move = (simulated_piece, (self.row, self.column), (new_row, new_col))

        # Execute the move on the copied board
        # if new_row != self.row or new_col != self.column:
        #     target_piece.die()
        #     simulated_board[new_row][new_col] = simulated_piece
        #     simulated_board[self.row][self.column] = ChessPiece()
        #     simulated_piece.row, simulated_piece.column = new_row, new_col
        simulated_piece.execute_move(simulated_board, new_row, new_col)

        # Find the king of the same color in the copied board
        king = self.find_king(simulated_board, self.color)

        # Check if the king is in check after the move
        is_in_check = self.is_king_in_check_for_castling(simulated_board, king, last_move)

        return not is_in_check
    
    def is_legal_move(self, board, new_row, new_col):
        """
        Checks if moving the piece to (new_row, new_col) is legal.
        A move is illegal if it puts the player's king in check.
        """
        # Create a deep copy of the board to simulate the move
        simulated_board = copy.deepcopy(board)

        # Find this piece in the copied board
        simulated_piece = simulated_board[self.row][self.column]
        # target_piece = simulated_board[new_row][new_col]

        # Record last_move
        last_move = (simulated_piece, (self.row, self.column), (new_row, new_col))

        # Execute the move on the copied board
        # if new_row != self.row or new_col != self.column:
        #     target_piece.die()
        #     simulated_board[new_row][new_col] = simulated_piece
        #     simulated_board[self.row][self.column] = ChessPiece()
        #     simulated_piece.row, simulated_piece.column = new_row, new_col
        simulated_piece.execute_move(simulated_board, new_row, new_col)

        # for row in simulated_board:
        #     print(" ".join(str(piece) for piece in row))

        # Find the king of the same color in the copied board
        king = self.find_king(simulated_board, self.color)
        if not king: 
            print(self.piece_type, self.row, self.column, new_row, new_col)

        # Check if the king is in check after the move
        is_in_check = self.is_king_in_check(simulated_board, king, last_move)

        return not is_in_check
    
    def get_valid_moves(self, board, last_move=None):
        pass

    def get_valid_moves_without_check(self, board, last_move=None):
        pass

    def execute_move(self, board, new_row, new_col, last_move=None, promoted_piece=PieceType.QUEEN):
        """
        Move the piece to (new_row, new_col) and update its state.
        """
        target_piece = board[new_row][new_col]

        # Ensure the move is valid: either an empty square or capturing an enemy piece
        if target_piece.piece_type == PieceType.NONE or target_piece.color != self.color:
            # Kill target piece
            target_piece.die()
            # Clear old position
            # board[self.row][self.column] = ChessPiece()
            ChessPiece().place_piece(board, self.row, self.column)
            # Move the rook
            self.row, self.column = new_row, new_col
            board[new_row][new_col] = self  # Place piece in new position
            # Mark as has_moved
            self.has_moved = True

        return board, target_piece if target_piece.piece_type != PieceType.NONE else None

    def place_piece(self, board, row, column):
        """
        Place the pawn at the specified position on the board.
        """
        self.row = row
        self.column = column
        board[row][column] = self  # Place piece on board

    def die(self):
        pass
    #     self.is_alive = False

    def reverse_color(self):
        if self.color:
            if self.color == PieceColor.WHITE:
                self.color = PieceColor.BLACK
            elif self.color == PieceColor.BLACK:
                self.color = PieceColor.WHITE

    def is_promotable(self, new_row):
        return False
    
    def can_castle(self, board, side):
        return False
