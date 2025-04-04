from .DrawRule import DrawRule
from ..ChessPiece import PieceType

class InsufficientMaterialRule(DrawRule):
    def __str__(self):
        return "Insufficient Material Draw"
    def __init__(self):
        self.TwoKingOnly = False
    def update(self, board, target_piece, moving_piece):
        size = len(board.board)
        for i in range(size):
            for j in range(size):
                if board[i][j].piece_type != PieceType.KING and board[i][j].piece_type != PieceType.NONE:
                    self.TwoKingOnly = False
                    return False
        self.TwoKingOnly = True
        return True
    def violate_rule(self):
        return self.TwoKingOnly
