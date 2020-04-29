%load_ext autoreload
%autoreload 2

from GameEngine import GameEngine
from RandomPlayer import RandomPlayer
from Heuristic.HillClimbPlayer import HillClimbPlayer
from Heuristic.SimulatedAnnealingPlayer import SimulatedAnnealingPlayer

players = [SimulatedAnnealingPlayer("SA1"), HillClimbPlayer("HC2")]

game = GameEngine(players)
game.play_games(10)

# game.init_game()
#
# game.players[0].hand
#
# game.players[0].decide_cards_to_discard(game)
# game.get_top_discard()
#
# game.players[0].intended_card_to_take
#
#
# discard_top = game.deck.draw_top_discard()
#
# discard_top
# game.players[0].add_cards_to_hand([discard_top])

#
# WANT: Expectiminimax
# Games: play 10 games, keep track of number of wins of each Player, and also running total points
# option to randomize positions
# # DEBUG:
