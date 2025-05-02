from .DrawRule import DrawRule
from ..ChessPiece import PieceType

class ThreeRepetitionRule(DrawRule):
    def __str__(self):
        return "Three Repetition Draw"
    def __init__(self):
        self.states = {}
        self.violate = False
    def update(self, board, target_piece, moving_piece):
        value = board.string_of_state_and_valid_moves()
        if value not in self.states:
            self.states[value] = 1
        else:
            self.states[value] = self.states[value] + 1
        if self.states[value] == 3:
            self.violate = True
        else:
            self.violate = False
    def violate_rule(self):
        return self.violate
