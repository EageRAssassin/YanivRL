from Player import Player
import math
import Helpers
import random

''' Player that randomly choose his play. '''
class RandomPlayer(Player):

    def decide_call_yaniv(self, game):
        if Helpers.get_hand_value(self.hand) <= 5:
            return True
        return False

    def decide_cards_to_discard(self, game):
        """A function that chooses to play randomly from all the playable strategies"""
        plays = self.show_plays()
        # there are (choices) random choices
        # we pick a random number from 0 to choice
        choice = random.uniform(0, len(plays))

        # TEMPORARY FEATURE, IF YANIV CAN BE CALLED, CALL YANIV
        if Helpers.get_hand_value(self.hand) <= 5:
            return []
        return plays[math.floor(choice)]

    def decide_cards_to_draw(self, game):
        ''' Randomly draw from either unseen pile or discard pile '''
        i = random.randint(0, 1)
        if i > 0:
            return "unseen_pile", None
        else:
            return "discard_pile", random.choice(game.get_top_discards())
