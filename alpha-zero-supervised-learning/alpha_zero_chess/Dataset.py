import torch
import numpy as np
import chess
import chess.pgn
from torch.utils.data import Dataset
import io

PIECE_PLANES = {
    'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
    'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11,
}

def encode_board(board: chess.Board) -> torch.Tensor:
    """Encode a chess.Board into a (16, 8, 8) tensor."""
    tensor = np.zeros((16, 8, 8), dtype=np.float32)
    
    # Pieces
    for square, piece in board.piece_map().items():
        row = 7 - (square // 8)
        col = square % 8
        plane = PIECE_PLANES[piece.symbol()]
        tensor[plane, row, col] = 1.0

    # Castling rights
    tensor[12][:][:] = 1.0 if board.has_kingside_castling_rights(chess.WHITE) else 0.0
    tensor[13][:][:] = 1.0 if board.has_kingside_castling_rights(chess.BLACK) else 0.0

    # Move count (normalize)
    tensor[14][:][:] = board.fullmove_number / 100.0

    # Side to move
    tensor[15][:][:] = 1.0 if board.turn == chess.WHITE else 0.0

    return torch.tensor(tensor)

def move_to_index(move: chess.Move) -> int:
    """Convert a move to an index (simplified 4672 policy space, 8x8x73)."""
    from_square = move.from_square
    to_square = move.to_square
    from_rank, from_file = divmod(from_square, 8)
    move_idx = from_rank * 8 * 73 + from_file * 73 + 0  # Simplified: pretend all moves go to first channel
    return move_idx

def result_to_value(result: str) -> float:
    """Map PGN result to a float value."""
    return {'1-0': 1.0, '0-1': -1.0, '1/2-1/2': 0.0}.get(result, 0.0)

class PGNDataset(Dataset):
    def __init__(self, pgn_path: str, max_games: int = 100):
        self.samples = []

        with open(pgn_path, "rb") as f_raw:
            # Read bytes, decode manually, then wrap with StringIO
            raw_data = f_raw.read().decode("utf-8-sig")  # auto-strips BOM
            f = io.StringIO(raw_data)  # wrap as text stream

            for _ in range(max_games):
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                result = result_to_value(game.headers["Result"])
                board = game.board()
                for move in game.mainline_moves():
                    x = encode_board(board)
                    y_policy = move_to_index(move)
                    y_value = result
                    self.samples.append((x, y_policy, y_value))
                    board.push(move)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        x, y_policy, y_value = self.samples[idx]
        return x, torch.tensor(y_policy), torch.tensor(y_value)

# dataset = PGNDataset("D:/y3t2/CCRL-404.[1542299].pgn/CCRL-404.[1542299].pgn", max_games=50)
# loader = DataLoader(dataset, batch_size=64, shuffle=True)

# for batch in loader:
#     x, policy_target, value_target = batch
#     print(x.shape)  # (batch_size, 16, 8, 8)
#     print(policy_target.shape)  # (batch_size,)
#     print(value_target.shape)   # (batch_size,)
#     break