import rlcard
import random
import functools
from rlcard.utils.utils import init_54_deck


class YanivDealer(rlcard.core.Dealer):
    """ Dealer stores a deck of playing cards, remained cards holded by dealer, and can deal cards to players
    Note: deck variable means all the cards in a single game, and should be a list of Card objects.
    """

    deck = []
    remained_cards = []

    def __init__(self):
        """ The dealer should have all the cards at the beginning of a game
        """
        super().__init__()
        self.deck = init_54_deck()

    def shuffle(self):
        """ Shuffle the cards holded by dealer(remained_cards)
        """
        random.shuffle(self.deck)

    def deal_cards(self, players):
        """ Deal specific number of cards to a specific player
        Args:
            player_id: the id of the player to be dealt cards
            num: number of cards to be dealt
        """

        hand_num = 7
        for index, player in enumerate(players):
            current_hand = self.deck[index*hand_num:(index+1)*hand_num]
            # TODO Sort Card
            # current_hand.sort(key=functools.cmp_to_key(doudizhu_sort_card))
            player.set_current_hand(current_hand)
            # TODO Need refinement
            # player.initial_hand = cards2str(player.current_hand)

