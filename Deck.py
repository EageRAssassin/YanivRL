import random
import Cards

class Deck:
    def __init__(self):
        self.cards = []
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

    def discard(self, cards):
        for card in previous_play:
            self.discards.append(card)

        if isinstance(cards, list):
            self.previous_play = cards
        else:
            self.previous_play = [cards]
        self.previous_play.sort(key = lambda c: c.sort_value())

    def get_top_discard(self):
        return [self.previous_play[0], self.previous_play[-1]] if len(self.previous_play) > 1 else self.previous_play
        # return self.discards[-1] if len(self.discards) > 0 else None

    def get_top_card(self):
        return self.cards[-1]

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
        self.previous_play = []
        return return_card

    def draw_top_card(self):
        if len(self.cards) == 1:
            last_card = self.cards.pop()
            self.remake_deck()
            return last_card
        return self.cards.pop()

    def remake_deck(self):
        top_discard = self.draw_top_discard()
        self.cards = self.discards
        self.discards = []
        self.shuffle()
        self.discards.append(top_discard)

    def get_cards(self):
        return self.cards

    def get_discards(self):
        return self.discards


if __name__ == '__main__':
    d = Deck()
    print(d.draw_top_card())
