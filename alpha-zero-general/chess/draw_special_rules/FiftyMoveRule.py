from .DrawRule import DrawRule
from ..ChessPiece import PieceType

class FiftyMoveRule(DrawRule):
    def __str__(self):
        return "Fifty Move Draw"
    def __init__(self):
        self.count = 0
    def update(self, board, target_piece, moving_piece):
        if target_piece or moving_piece == PieceType.PAWN:
            self.count = 0
        else: 
            self.count = self.count + 1
    def violate_rule(self):
        return self.count >= 50
