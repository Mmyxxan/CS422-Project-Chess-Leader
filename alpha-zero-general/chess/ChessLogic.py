from .ChessPiece import ChessPiece
from .ChessPiece import PieceType
from .ChessPiece import PieceColor
from .pieces.Pawn import Pawn
from .pieces.Bishop import Bishop
from .pieces.King import King
from .pieces.Knight import Knight
from .pieces.Queen import Queen
from .pieces.Rook import Rook
from enum import Enum

class GameState(Enum):
    IN_PROGRESS = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3
    DRAW = 4

class Board:
    BOARD_SIZE = 8
    PAWN_SIZE = BOARD_SIZE
    ROOK_SIZE = BISHOP_SIZE = KNIGHT_SIZE = 2
    QUEEN_SIZE = KING_SIZE = 1

    def __init__(self):
        self.state = (GameState.IN_PROGRESS, PieceColor.NONE)
        self.board = [[ChessPiece() for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.last_move = None
        self.initialize_board()

    def initialize_board(self):
        """
        Initializes the chessboard with pieces in their standard positions.
        """
        # ChessPiece()'s place piece for king & bishop already else not modified
        # Empty cell has color too
        self.board = [[ChessPiece() for _ in range(8)] for _ in range(8)]  # Fill board with blank ChessPiece objects

        # Placing Pawns
        for i in range(8):
            self.board[6][i] = Pawn(color=PieceColor.WHITE, row=6, column=i)
            self.board[1][i] = Pawn(color=PieceColor.BLACK, row=1, column=i)

        # Placing Rooks
        self.board[7][0] = Rook(color=PieceColor.WHITE, row=7, column=0)
        self.board[7][7] = Rook(color=PieceColor.WHITE, row=7, column=7)
        self.board[0][0] = Rook(color=PieceColor.BLACK, row=0, column=0)
        self.board[0][7] = Rook(color=PieceColor.BLACK, row=0, column=7)

        # Placing Knights
        self.board[7][1] = Knight(color=PieceColor.WHITE, row=7, column=1)
        self.board[7][6] = Knight(color=PieceColor.WHITE, row=7, column=6)
        self.board[0][1] = Knight(color=PieceColor.BLACK, row=0, column=1)
        self.board[0][6] = Knight(color=PieceColor.BLACK, row=0, column=6)

        # Placing Bishops
        self.board[7][2] = Bishop(color=PieceColor.WHITE, row=7, column=2)
        self.board[7][5] = Bishop(color=PieceColor.WHITE, row=7, column=5)
        self.board[0][2] = Bishop(color=PieceColor.BLACK, row=0, column=2)
        self.board[0][5] = Bishop(color=PieceColor.BLACK, row=0, column=5)

        # Placing Queens
        self.board[7][3] = Queen(color=PieceColor.WHITE, row=7, column=3)
        self.board[0][3] = Queen(color=PieceColor.BLACK, row=0, column=3)

        # Placing Kings
        self.board[7][4] = King(color=PieceColor.WHITE, row=7, column=4)
        self.board[0][4] = King(color=PieceColor.BLACK, row=0, column=4)

    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.board[index]

    def get_legal_moves(self, color=PieceColor.NONE):
        size = len(self.board)
        move_matrix = [[[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)] for _ in range(size)]
        # state, color = self.state
        # if state == GameState.CHECK:
        #     random_piece = self.board[0][0]
        #     king = random_piece.find_king(self.board, color)
        #     move_matrix[king.row][king.column] = king.get_valid_moves(self.board, self.last_move)
        # else:
        #     for i in range(size):
        #         for j in range(size):
        #             if self.board[i][j].piece_type != PieceType.NONE:
        #                 move_matrix[i][j] = self.board[i][j].get_valid_moves(self.board, self.last_move)
        for i in range(size):
            for j in range(size):
                if self.board[i][j].piece_type != PieceType.NONE:
                    if color == PieceColor.NONE or self.board[i][j].color == color:
                        move_matrix[i][j] = self.board[i][j].get_valid_moves(self.board, self.last_move)
        return move_matrix

    def has_legal_moves(self, color):
        matrix = self.get_legal_moves()
        size = len(self.board)
        for i in range(size):
            for j in range(size):
                for r in range(size):
                    for c in range(size):
                        if matrix[i][j][r][c] and (color == PieceColor.NONE or self.board[i][j].color == color):
                            return True
        return False

    def execute_move(self, piece, new_row, new_col, promoted_piece=PieceType.QUEEN):
        # Update self.last_move
        self.last_move = (piece, (piece.row, piece.column), (new_row, new_col))
        # Execute the move
        piece.execute_move(self.board, new_row, new_col, self.last_move, promoted_piece)
        # Update the game state
        king = piece.find_king(self.board, PieceColor.WHITE if piece.color == PieceColor.BLACK else PieceColor.BLACK)
        if piece.is_king_in_check(self.board, king, self.last_move):
            self.state = (GameState.CHECK, PieceColor.WHITE if piece.color == PieceColor.BLACK else PieceColor.BLACK)
            if not self.has_legal_moves(PieceColor.WHITE if piece.color == PieceColor.BLACK else PieceColor.BLACK):
                self.state = (GameState.CHECKMATE, PieceColor.WHITE if piece.color == PieceColor.BLACK else PieceColor.BLACK)
        elif not self.has_legal_moves(PieceColor.WHITE if piece.color == PieceColor.BLACK else PieceColor.BLACK):
            self.state = (GameState.STALEMATE, PieceColor.NONE)
        else:
            self.state = (GameState.IN_PROGRESS, PieceColor.NONE)
            # self.state = (GameState.DRAW, PieceColor.NONE)

    def get_game_state(self):
        """Returns the game state and the color of the player affected (if applicable)."""
        return self.state

    def print_board(self):
        for row in self.board:
            print(" ".join(str(piece) for piece in row))

    def print_board_with_grid(self):
        """Prints the board with labeled rows and columns for easier gameplay."""
        column_labels = "  a b c d e f g h"
        print(column_labels)
        print("  -----------------")
        for i, row in enumerate(self.board):
            row_str = f"{8 - i}|" + " ".join(str(piece) if str(piece) != "." else "." for piece in row)
            print(row_str)
        print("  -----------------")
        print(column_labels)

    def get_board_matrix(self):
        """Returns the board as a matrix of strings."""
        return [[str(piece) if piece else "." for piece in row] for row in self.board]
    
    def reverse_board(self):
        size = len(self.board)
        for i in range(size):
            for j in range(size):
                self.board[i][j].reverse_color()

    def is_win(self, player):
        return self.state[0] == GameState.CHECKMATE and self.state[1] == PieceColor.BLACK if player == 1 else self.state[0] == GameState.CHECKMATE and self.state[1] == PieceColor.WHITE
    
    def is_draw(self):
        return self.state[0] == GameState.STALEMATE
    
    def is_in_progress(self):
        return self.state[0] == GameState.IN_PROGRESS or self.state[0] == GameState.CHECK
