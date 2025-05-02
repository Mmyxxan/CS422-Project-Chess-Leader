import Arena
from MCTS import MCTS
from chess.ChessGame import ChessGame
from chess.ChessPlayers import *
from chess.pytorch.ChessNNet import ChessNNet
import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

args = dotdict({
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'cpuct': 1,
})

class AlphaZeroPlayer():
    def __init__(self, game):
        self.game = game
        self.nnet = ChessNNet(self.game)
        self.args = args
        self.mcts = MCTS(self.game, self.nnet, self.args)

    def play(self, board):
        pi = self.mcts.getActionProb(board, temp=0)
        valids = self.game.getValidMoves(board, 1)
        a = np.random.choice(len(pi), p=pi)
        while valids[a]!=1:
            a = np.random.choice(len(pi), p=pi)
        return a

cpu_vs_cpu = True

g = ChessGame()

# all players
rp1 = HumanChessPlayer(g).play
rp2 = HumanChessPlayer(g).play

if cpu_vs_cpu:
    player2 = rp2
    player1 = rp1

arena = Arena.Arena(player1, player2, g, display=ChessGame.displayGrid)

print(arena.playGames(2, verbose=True))
