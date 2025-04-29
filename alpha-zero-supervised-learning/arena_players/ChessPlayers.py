import numpy as np
import chess
from .move_index import *
from alpha_zero_chess.utils import *
from alpha_zero_chess.ChessNNet import ChessNNet
import torch
from .MCTS import MCTS

nnet_args = dotdict({
    'best_model_folder': '../alpha-zero-supervised-learning/model/',
    'best_model_filename': 'best_model_20x256.pth',
    # 'best_model_filename': 'AlphaZeroNet_20x256.pt',
    'epochs': 40,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'folder': 'model/',
    'filename': 'chess_nnet_ccrl.pth',
    'max_games_training': 70000,
    'max_games_debugging': 20
})

args = dotdict({
    'numMCTSSims': 400,          # Number of games moves for MCTS to simulate, draw chess.com 1000.
    'cpuct': 1,
})

class AlphaZeroPlayer():
    def __init__(self, game):
        self.game = game
        self.args = args
        self.nnet_args = nnet_args
        self.nnet = ChessNNet(self.nnet_args)
        self.mcts = MCTS(self.game, self.nnet, self.args)

    def play(self, board, curPlayer):
        canonicalBoard = self.game.getCanonicalForm(board, curPlayer)
        pi = self.mcts.getActionProb(canonicalBoard, temp=0)
        action = np.random.choice(len(pi), p=pi)
        if curPlayer == -1:
            from_square_index = action // 73
            direction_channel = action % 73

            from_rank = 7 - from_square_index // 8
            from_file = from_square_index % 8

            if direction_channel not in MoveDirection73.get_promotion_indices():
                dr, dc = MoveDirection73.get(direction_channel)
                dr = -dr
                direction_channel = MoveDirection73.index(dr, dc)

            return (from_rank*8+from_file)*73 + direction_channel
        return action

class RandomPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board, curPlayer):
        valids = list(board.legal_moves)  # convert generator to list
        while True:
            a = np.random.randint(self.game.getActionSize())
            move = index_to_move(a, board)  # pass board as argument
            if move in valids:
                return a

class HumanChessPlayer:
    def __init__(self, game):
        self.game = game

    def play(self, board: chess.Board, curPlayer):
        while True:
            move_input = input("Enter your move (e.g., e2e4 or e7e8n): ").strip().lower()

            if len(move_input) < 4 or len(move_input) > 5:
                print("❌ Invalid format. Use e2e4 or e7e8n.")
                continue

            try:
                from_square = chess.parse_square(move_input[:2])
                to_square = chess.parse_square(move_input[2:4])
                promotion = None

                if len(move_input) == 5:
                    promo_map = {
                        'q': chess.QUEEN,
                        'r': chess.ROOK,
                        'b': chess.BISHOP,
                        'n': chess.KNIGHT
                    }
                    promo_char = move_input[4]
                    if promo_char not in promo_map:
                        print("❌ Invalid promotion piece. Use q, r, b, or n.")
                        continue
                    promotion = promo_map[promo_char]

                move = chess.Move(from_square, to_square, promotion=promotion)

                if move not in board.legal_moves:
                    print("❌ Illegal move. Try again.")
                    continue

                index = move_to_index(move)
                if index == -1:
                    print("❌ Move not supported by policy space.")
                    continue

                return index

            except Exception:
                print("❌ Could not parse move. Try again.")
