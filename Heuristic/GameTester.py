%load_ext autoreload
%autoreload 2

from GameEngine import GameEngine
from RandomPlayer import RandomPlayer
from Heuristic.HillClimbPlayer import HillClimbPlayer
from Heuristic.SimulatedAnnealingPlayer import SimulatedAnnealingPlayer

players = [HillClimbPlayer("HA1"), HillClimbPlayer("HC2"), RandomPlayer("RP")]

game = GameEngine(players)
game.play_games(1)

# game.init_game()
#
# game.players[0].hand
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
