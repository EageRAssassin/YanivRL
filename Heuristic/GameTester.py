%load_ext autoreload
autoreload 2

from GameEngine import GameEngine
from RandomPlayer import RandomPlayer
from Heuristic.HillClimbPlayer import HillClimbPlayer
from Heuristic.SimulatedAnnealingPlayer import SimulatedAnnealingPlayer
from Heuristic.MinimaxPlayer import MinimaxPlayer


R1 = RandomPlayer("R1")
R2 = RandomPlayer("R2")
R3 = RandomPlayer("R3")
R4 = RandomPlayer("R4")

HC1= HillClimbPlayer("HC1")
HC2= HillClimbPlayer("HC2")
HC3= HillClimbPlayer("HC3")
HC4= HillClimbPlayer("HC4")

SA1= SimulatedAnnealingPlayer("SA1")
SA2= SimulatedAnnealingPlayer("SA2")
SA3= SimulatedAnnealingPlayer("SA3")
SA4= SimulatedAnnealingPlayer("SA4")

M1= MinimaxPlayer("M1")
M2= MinimaxPlayer("M2")
M3= MinimaxPlayer("M3")
M4= MinimaxPlayer("M4")

players = [HC1, M1, SA1]

game = GameEngine(players)

game.play_games(10)

# game.init_game()
#
# game.get_state(0)
#
# game.players[0].hand
#
# game.players[0].decide_cards_to_discard(game)
# game.get_top_discard()
#
# game.players[0].intended_card_to_take
#
# discard_top = game.deck.draw_top_discard()
#
# discard_top
# game.players[0].add_cards_to_hand([discard_top])
#
# a = 1 % 3
# 3%3
#
# self.history= [(0,[play],card_taken), (1,[play],card_taken),()]
