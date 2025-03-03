from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .ChessLogic import Board
from .ChessPiece import PieceColor, PieceType
import numpy as np
import copy

class ChessGame(Game):
    """
    White is 1, Black is -1
    """
    promotion_pieces = [PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK, PieceType.QUEEN]
    PROMOTION_SIZE = len(promotion_pieces)
    NUMS_CHUNK = (8 ** 2) * (8 ** 2)

    def __init__(self):
        pass

    def getInitBoard(self):
        b = Board()
        return b

    def getBoardSize(self):
        return 8

    def getActionSize(self):
        return (8 ** 2) * (8 ** 2) * self.PROMOTION_SIZE

    def getNextState(self, board, player, action):
        board_size = len(board.board)
        b = copy.deepcopy(board)
        chunk = (8 ** 2) * (8 ** 2)
        r_action = action % chunk
        promoted_piece = self.promotion_pieces[action // chunk] if action // chunk > 0 else None
        cell = int(r_action / (board_size ** 2))
        move = r_action % (board_size ** 2)

        piece, new_row, new_col = b.board[int(cell / board_size)][cell % board_size], int(move / board_size), move % board_size
        b.execute_move(piece, new_row, new_col, promoted_piece)

        return (b, -player)

    def getValidMoves(self, board, player):
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

    def getGameEnded(self, board, player):
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

    def getSymmetries(self, board, pi):
        pass

    def stringRepresentation(self, board):
        return board.get_board_matrix()
    
    @staticmethod
    def display(board):
        board.print_board()

    @staticmethod
    def displayGrid(board):
        board.print_board_with_grid()
