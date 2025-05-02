import chess
from enum import Enum

class PieceType(Enum):
    NONE = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

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

def move_to_index(move: chess.Move) -> int:
    from_square = move.from_square
    to_square = move.to_square
    from_rank, from_file = divmod(from_square, 8)
    to_rank, to_file = divmod(to_square, 8)

    dr = to_rank - from_rank
    dc = to_file - from_file

    # Check if this is an underpromotion (excluding Queen)
    if move.promotion and move.promotion != chess.QUEEN:
        if dc == 0:
            base = 64  # forward
        elif dc == -1:
            base = 67  # left
        elif dc == 1:
            base = 70  # right
        else:
            return -1  # invalid promotion direction

        if move.promotion == chess.KNIGHT:
            offset = 0
        elif move.promotion == chess.BISHOP:
            offset = 1
        elif move.promotion == chess.ROOK:
            offset = 2
        else:
            return -1  # unsupported promotion

        direction_channel = base + offset
    else:
        direction_channel = MoveDirection73.index(dr, dc)
        if direction_channel == -1:
            return -1  # invalid move direction

    # Flattened index: (from_rank * 8 + from_file) * 73 + direction_channel
    return from_rank * 8 * 73 + from_file * 73 + direction_channel

def index_to_move(index: int, board: chess.Board) -> chess.Move:
    """
    Converts a flattened action index (0 to 4671) back to a chess.Move object.
    Uses `MoveDirection73.translate_move` for accurate target square and promotion.
    """
    from_square_index = index // 73
    direction_channel = index % 73

    from_rank = from_square_index // 8
    from_file = from_square_index % 8
    from_square = chess.square(from_file, from_rank)  # python-chess uses 0=bottom rank

    # Build a lightweight piece object with required info
    class FakePiece:
        def __init__(self, row, column, direction):
            self.row = row
            self.column = column
            self.direction = -1  # always -1 for black's promotion by default, black going down
            if board.piece_at(from_square) and board.piece_at(from_square).color == chess.WHITE:
                self.direction = 1  # white promotes going up

    piece = FakePiece(from_rank, from_file, 0)  # direction set inside

    to_rank, to_file, promoted_piece_type = MoveDirection73.translate_move(piece, direction_channel)

    # Make sure it's in bounds
    if not (0 <= to_rank < 8 and 0 <= to_file < 8):
        return chess.Move.null()

    to_square = chess.square(to_file, to_rank)

    # Convert PieceType to chess.promotion constant
    if board.piece_at(from_square) and board.piece_at(from_square).piece_type == chess.PAWN and (to_rank == 0 or to_rank == 7):
        promotion = chess.QUEEN
    else:
        promotion = None
    if direction_channel in MoveDirection73.get_promotion_indices():
        if promoted_piece_type == PieceType.KNIGHT:
            promotion = chess.KNIGHT
        elif promoted_piece_type == PieceType.BISHOP:
            promotion = chess.BISHOP
        elif promoted_piece_type == PieceType.ROOK:
            promotion = chess.ROOK

    return chess.Move(from_square, to_square, promotion=promotion)

# move = chess.Move.from_uci("e2e4")
# index = move_to_index(move)
# move = index_to_move(877, chess.Board())
# print(move)
# print(index)  # Example: 877

# move = chess.Move.from_uci("g7g8n")  # underpromote to Knight
# index = move_to_index(move)
# move = index_to_move(4006, chess.Board())
# print(move)
# print(index)  # Should be in 64–72