from arena_players.Arena import Arena
from arena_players.ChessPlayers import *
from arena_players.ChessGame import ChessGame

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

cpu_vs_cpu = True

g = ChessGame()

# all players
rp1 = AlphaZeroPlayer(g).play
rp2 = RandomPlayer(g).play

if cpu_vs_cpu:
    player2 = rp2
    player1 = rp1

arena = Arena(player1, player2, g, display=ChessGame.display)

print(arena.playGames(2, verbose=True))
