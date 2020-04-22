%load_ext autoreload
%autoreload 2

from GameEngine import GameEngine
from Heuristic.HillClimbPlayer import HillClimbPlayer
import Heuristic.SimulatedAnnealingPlayer as SimulatedAnnealingPlayer


players = [HillClimbPlayer("HC1"), HillClimbPlayer("HC2")]

game = GameEngine(players)
