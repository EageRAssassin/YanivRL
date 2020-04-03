import rlcard


class Player(rlcard.core.Player):
    """ Player stores cards in the player's hand, and can determine the actions can be made according to the rules
    """

    player_id = None
    hand = []

    def __init__(self, player_id):
        """ Every player should have a unique player id
        """
        self.player_id = player_id
        self.initial_hand = None
        self._current_hand = []
        self.played_cards = None

    def available_order(self, prev_player=None):
        """ Get the actions can be made based on the rules
        Returns:
            list: a list of available orders
        """
        actions = []

        # need to translate this into the RL type
        # plays = []
        # for card in self.hand:
        #     plays.append([card])
        # # find the choices for a pair
        # for i in range(len(self.hand) - 1):
        #     if self.hand[i].value == self.hand[i + 1].value:
        #         plays.append([self.hand[i], self.hand[i + 1]])
        #     # the choices for a straight
        # for i in range(len(self.hand) - 2):
        #     for j in range(i, len(self.hand) - 1):
        #         for k in range(j, len(self.hand)):
        #             if self.hand[i].value + 2 == self.hand[j].value + 1 == self.hand[k].value \
        #                     and self.hand[i].suit == self.hand[j].suit == self.hand[k].suit:
        #                 plays.append([self.hand[i], self.hand[j], self.hand[k]])
        # TODO to incorpate get card from table function

        return actions

    def play(self, action, prev_player=None):
        """ Player's actual action in the round
        """
        raise NotImplementedError