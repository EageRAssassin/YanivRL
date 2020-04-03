import rlcard

from ReinforcementLearning.RLCard.core.dealer import YanivDealer


class YanivRound(rlcard.core.Round):
    """ Round stores the id the ongoing round and can call other Classes' functions to keep the game running
        """

    def __init__(self):
        """ When the game starts, round id should be 1
        """
        self.trace = []
        self.greater_player = None
        self.dealer = YanivDealer()

    def proceed_round(self, **kwargs):
        """ Call other Classes's functions to keep the game running
        """
        raise NotImplementedError