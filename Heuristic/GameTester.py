%load_ext autoreload
autoreload 2

from GameEngine import GameEngine
from RandomPlayer import RandomPlayer
from Heuristic.HillClimbPlayer import HillClimbPlayer
from Heuristic.SimulatedAnnealingPlayer import SimulatedAnnealingPlayer
from Heuristic.MinimaxPlayer import MinimaxPlayer


RandPlayer = RandomPlayer("Random")
HCPlayer= HillClimbPlayer("Hill Climbing")
SAPlayer= SimulatedAnnealingPlayer("Simulated Annealing")
MMPlayer= MinimaxPlayer("Minimax")

game = GameEngine([RandPlayer, SAPlayer, MMPlayer, HCPlayer])


game.play_games(1,True)

#parameters are num_rounds, print_verbose, shuffle_player_order
game = GameEngine([RandPlayer, SAPlayer, MMPlayer, HCPlayer])
scores, wins = game.play_games(1000,False, True)
scores
wins

# game = GameEngine([SAPlayer, HCPlayer])
# scores, wins = game.play_games(1000,False)
# scores
# wins
#
#
# game = GameEngine([MMPlayer, HCPlayer])
# scores, wins = game.play_games(1000,False)
# scores
# wins
#
# game = GameEngine([SAPlayer, MMPlayer])
# scores, wins = game.play_games(1000,False)
# scores
# wins
