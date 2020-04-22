import random
import Cards

class Deck:
    def __init__(self):
        self.cards = []
        self.current_play = []
        self.previous_play = []
        self.discards = []
        for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
            for rank in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
                self.cards.append(Cards.Card(rank, suit))
        self.cards.append(Cards.Card(0, ''))
        self.cards.append(Cards.Card(0, ''))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    # The Yaniv turn loop is as follows:
    # 1) Discard card(s) into the current_play "holding area"
    # 2) Take a card, either from the previous_play "previous player's play" or from the self.cards "deck"
    # 3) Move the previous_play into the discards, then move the current_play into the previous_play

    # discard() handles Step 1 by putting the cards to be discarded into the current_play pile
    def discard(self, cards):
        """ Note: This part should be step 3
        for card in previous_play:
            self.discards.append(card)
        """
        if isinstance(cards, list):
            self.current_play = cards
        else:
            self.current_play = [cards]
        self.current_play.sort(key = lambda c: c.sort_value())
        #self.previous_play.sort(key = lambda c: c.sort_value())

    def get_top_discard(self):
        return [self.previous_play[0], self.previous_play[-1]] if len(self.previous_play) > 1 else self.previous_play
        # return self.discards[-1] if len(self.discards) > 0 else None

    def get_top_card(self):
        return self.cards[-1]

    # draw_top_discard(), in the draw-from-discard case, handles Steps 2 and 3 simultaneously by taking the appropriate card
    # from the previous_play pile, moving any remaining cards from previous_play into the general discards pile,
    # then setting the current_play as the previous_play
    def draw_top_discard(self, card = None):
        if (len(self.previous_play)) == 1:
            return_card = self.previous_play[0]
        elif card in [self.previous_play[0], self.previous_play[-1]]:
            self.previous_play.remove(card)
            for c in self.previous_play:
                self.discards.append(c)
            return_card = card
        else:
            raise CardNotExistInPreviousPlayError()
        self.previous_play = self.current_play
        return return_card

    # draw_top_card(), in the draw-from-deck case, handles Steps 2 and 3 simultaneously by popping the top card
    # from the deck, then moving the previous_play to the discards pile, then setting the current_play as the previous_play
    # If the deck is fully drawn, then the current_play becomes the new "discard pile" (note that, since it is also the previous_play,
    # it does not actually join the discards piile until it is moved out of the previous_play pile in some way)

    def draw_top_card(self):
        last_card = self.cards.pop()
        for c in self.previous_play:
            self.discards.append(c)
        self.previous_play = self.current_play
        if len(self.cards) == 0:
            self.remake_deck()
        return last_card

    def remake_deck(self):
        self.cards = self.discards
        self.discards = []
        self.shuffle()

    def get_cards(self):
        return self.cards

    def get_discards(self):
        return self.discards


if __name__ == '__main__':
    d = Deck()
    print(d.draw_top_card())
