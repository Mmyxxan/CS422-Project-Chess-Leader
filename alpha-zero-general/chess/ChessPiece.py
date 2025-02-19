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

class ChessPiece:
    def __init__(self, piece_type=PieceType.NONE, color=PieceColor.NONE, row=-1, column=-1):
        self.piece_type = piece_type
        self.color = color
        self.row = row
        self.column = column
        self.is_alive = True
        self.has_moved = False

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
        return None
    
    def is_king_in_check_for_castling(self, board, king, last_move=None):
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j].piece_type != PieceType.KING and board[i][j].piece_type != PieceType.NONE and board[i][j].color != king.color and board[i][j].get_valid_moves_without_check(board, last_move)[king.row][king.column]:
                    return True
                elif board[i][j].piece_type == PieceType.KING and board[i][j].color != king.color:
                    opponent_king = board[i][j]
                    if opponent_king.has_moved:
                        if opponent_king.get_valid_moves_without_check(board, last_move)[king.row][king.column]:
                            return True
        return False
                
    def is_king_in_check(self, board, king, last_move=None):
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j].piece_type != PieceType.NONE and board[i][j].color != king.color and board[i][j].get_valid_moves_without_check(board, last_move)[king.row][king.column]:
                    return True
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
        target_piece = simulated_board[new_row][new_col]

        # Record last_move
        last_move = (simulated_piece, (self.row, self.column), (new_row, new_col))

        # Execute the move on the copied board
        if new_row != self.row or new_col != self.column:
            target_piece.die()
            simulated_board[new_row][new_col] = simulated_piece
            simulated_board[self.row][self.column] = ChessPiece()
            simulated_piece.row, simulated_piece.column = new_row, new_col

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
        target_piece = simulated_board[new_row][new_col]

        # Record last_move
        last_move = (simulated_piece, (self.row, self.column), (new_row, new_col))

        # Execute the move on the copied board
        if new_row != self.row or new_col != self.column:
            target_piece.die()
            simulated_board[new_row][new_col] = simulated_piece
            simulated_board[self.row][self.column] = ChessPiece()
            simulated_piece.row, simulated_piece.column = new_row, new_col

        # Find the king of the same color in the copied board
        king = self.find_king(simulated_board, self.color)

        # Check if the king is in check after the move
        is_in_check = self.is_king_in_check(simulated_board, king, last_move)

        return not is_in_check
    
    def get_valid_moves(self, board, last_move=None):
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
            board[self.row][self.column] = ChessPiece()
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
        self.is_alive = False

    def reverse_color(self):
        if self.color:
            if self.color == PieceColor.WHITE:
                self.color = PieceColor.BLACK
            else:
                self.color = PieceColor.WHITE

    def is_promotable(self, new_row):
        return False
