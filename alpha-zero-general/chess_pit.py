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

human_vs_cpu = True

g = ChessGame()

# all players
rp = RandomPlayer(g).play
hp = HumanChessPlayer(g).play

if human_vs_cpu:
    player2 = hp
    player1 = rp

arena = Arena.Arena(player1, player2, g, display=ChessGame.display)

print(arena.playGames(2, verbose=True))
