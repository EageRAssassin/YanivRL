from Player import Player
import math
import random

''' Player that randomly choose his play. '''
class RandomPlayer(Player):

    def decide_call_yaniv(self, game):
        if self.get_hand_value() <= 5:
            return True
        return False

    def decide_cards_to_discard(self, game):
        """A function that chooses to play randomly from all the playable strategies"""
        plays = self.show_plays()
        # there are (choices) random choices
        # we pick a random number from 0 to choice
        choice = random.uniform(0, len(plays))
        return plays[math.floor(choice)]

    def decide_cards_to_draw(self, game):
        ''' Randomly draw from either unseen pile or discard pile '''
        i = random.randint(0, 1)
        if i > 0:
            return "unseen_pile", [game.get_top_card()]
        else:
            return "discard_pile", [game.get_top_discard()]