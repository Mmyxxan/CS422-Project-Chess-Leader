from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .ChessLogic import Board
from .ChessPiece import PieceColor, PieceType, MoveDirection73
import numpy as np
import copy

class ChessGame(Game):
    """
    White is 1, Black is -1
    """
    # promotion_pieces = [PieceType.QUEEN, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
    # PROMOTION_SIZE = len(promotion_pieces)
    # NUMS_CHUNK = 8 * 8

    def __init__(self):
        # self.step = 0
        self.STEP_LIMIT = 140
        pass

    def getInitBoard(self):
        b = Board()
        # self.step = 0
        return b

    def getBoardSize(self):
        return 8

    def getActionSize(self):
        return 8 * 8 * 73
        # return (8 ** 2) * (8 ** 2) * self.PROMOTION_SIZE

    def getNextState(self, board, player, action):
        board_size = len(board.board)
        b = copy.deepcopy(board)
        cell = int(action / 73)
        piece = b.board[int(cell / board_size)][cell % board_size]

        r_action = action % 73
        dr, dc = MoveDirection73.get(r_action)
        new_row = piece.row + dr
        new_col = piece.column + dc
        promoted_piece = PieceType.QUEEN

        # print(r_action, piece, piece.row, piece.column)

        if r_action in MoveDirection73.get_promotion_indices():
            dr, dc = piece.direction, MoveDirection73.get(r_action)[1]
            new_row = piece.row + dr
            new_col = piece.column + dc
            promoted_piece = MoveDirection73.get_promotion_piece(r_action)
        
        # print(piece.piece_type, piece.row, piece.column, new_row, new_col)
        b.execute_move(piece, new_row, new_col, promoted_piece)

        # self.step = self.step + 1

        # self.display(b)

        return (b, -player)

    def getValidMoves(self, board, player):
        return board.get_legal_moves(PieceColor.WHITE if player == 1 else PieceColor.BLACK)
        # should be modified to contain valid pawn promotions
        valids = [0]*self.getActionSize()
        legalMoves =  board.get_legal_moves(PieceColor.WHITE if player == 1 else PieceColor.BLACK)
        board_size = len(board.board)
        for chunk in range (self.PROMOTION_SIZE):
            for i in range(board_size):
                for j in range(board_size):
                    for r in range(board_size):
                        for c in range(board_size):
                            if legalMoves[i][j][r][c]:
                                if chunk == 0:
                                    valids[(board_size ** 2) * (board_size * i + j) + board_size * r + c + chunk * self.NUMS_CHUNK] = 1
                                else: 
                                    if board[i][j].is_promotable(r):
                                        valids[(board_size ** 2) * (board_size * i + j) + board_size * r + c + chunk * self.NUMS_CHUNK] = 1
                                    else:
                                        valids[(board_size ** 2) * (board_size * i + j) + board_size * r + c + chunk * self.NUMS_CHUNK] = 0
        return np.array(valids)

    def getGameEnded(self, board, player, step):
        if step and step >= self.STEP_LIMIT:
            # print("EXCEED STEP LIMIT")
            return 1e-4
        if board.is_in_progress():
            return 0
        if board.is_win(player):
            return player
        if board.is_win(-player):
            return -player
        return 1e-4

    def getCanonicalForm(self, board, player):
        canonical_board = copy.deepcopy(board)
        canonical_board.reverse_board()
        return canonical_board if player == -1 else board

    def getSymmetries_(self, board, pi):
        # generate white side board, black side board of the same example and the corresponding policy
        # for data augmentation and diversity
        # map: 
        # horizontal flip: row i -> 7 - i
        # 90 degree: right
        # 270 degree: left
        # 180 degree: row i -> 7 - i, column i -> 7 - i
        # vertical flip: column i -> 7 - i
        symmetries = []
        board_size = len(board.board)  # Assuming it's 8x8
        # board_reshaped = np.array(board).reshape((board_size, board_size))
        board_reshaped = np.array(board.board)   # Board is not flattened
        
        # Convert policy back to matrix form
        pi_array = np.array(pi)  # Convert to NumPy array
        pi_matrix = pi_array.reshape((board_size, board_size, board_size, board_size, self.PROMOTION_SIZE))

        # Generate symmetries (rotations and flips)
        for rot in range(4):  # Rotations: 0°, 90°, 180°, 270°
            rotated_board = np.rot90(board_reshaped, k=rot)
            rotated_pi = np.rot90(pi_matrix, k=rot, axes=(0, 1))  # Rotate moving piece
            rotated_pi = np.rot90(rotated_pi, k=rot, axes=(2, 3))  # Rotate destination
            
            # symmetries.append((rotated_board.flatten(), rotated_pi.flatten()))
            symmetries.append((rotated_board, rotated_pi.flatten()))
            
            # Flipping the board horizontally. What about vertically, -v?
            flipped_board = np.fliplr(rotated_board)
            flipped_pi = np.fliplr(rotated_pi)
            # symmetries.append((flipped_board.flatten(), flipped_pi.flatten()))
            symmetries.append((flipped_board, flipped_pi.flatten()))

            # After the horizontal flip and rotation code:
            flipped_vertical_board = np.flipud(rotated_board)  # Flip vertically (up-down)
            flipped_vertical_pi = np.flipud(rotated_pi)  # Flip policy vertically

            # Add the flipped vertical versions to the list of symmetries
            symmetries.append((flipped_vertical_board, flipped_vertical_pi.flatten()))
        
        return symmetries
    
    def getSymmetries(self, board, pi):
        symmetries = []
        symmetries.append((board.board, pi))
        return symmetries

    def stringRepresentation(self, board):
        return tuple(tuple(row) for row in board.get_board_matrix())
    
    @staticmethod
    def display(board):
        board.print_board()

    @staticmethod
    def displayGrid(board):
        board.print_board_with_grid()

    @staticmethod
    def can_castle(board, color, side):
        king = board[0][0].find_king(board, color)
        return king.can_castle(board, side)
