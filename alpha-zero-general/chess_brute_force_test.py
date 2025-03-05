import Arena
from MCTS import MCTS
from chess.ChessGame import ChessGame
from chess.ChessPlayers import *
from othello.pytorch.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

cpu_vs_cpu = True

g = ChessGame()

# all players
rp1 = RandomPlayer(g).play
rp2 = RandomPlayer(g).play

if cpu_vs_cpu:
    player2 = rp2
    player1 = rp1

arena = Arena.Arena(player1, player2, g, display=ChessGame.displayGrid)

print(arena.playGames(2, verbose=True))
