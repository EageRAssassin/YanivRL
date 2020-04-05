from Player import Player

class BasePlayer(Player):

    def __init__(self, id):
        super().__init__(id)

    def decide_cards_to_discard(self, game):
        plays = self.show_plays()
        plays.sort(key=lambda lst: -sum([y.value for y in lst]))
        return plays[0]

    def decide_cards_to_draw(self, game):
        pass

    def decide_call_yaniv(self, game):
        if self.get_hand_value() <= 5:
            return True
        return False

    def decide_cards_to_draw2(self, cards):
        """A  function that chooses to discard randomly from all the playable strategies"""
        card_to_take = None
        # if joker is thrown, take it
        for c in cards:
            if c.value == 0:
                card_to_take = c
                self.add_cards_to_hand([card_to_take])
                return card_to_take
        # take card from the cards
        for c in reversed(cards):
            # there exist a card with same suit and one smaller value
            for h1 in self.hand:
                # there exist a card with same suit and one larger value
                for h2 in self.hand:
                    if h1.value != 0 and h2.value != 0:
                        # c < h1 < h2
                        if c.value + 2 == h1.value + 1 == h2.value and c.suit == h1.suit == h2.suit:
                            card_to_take = c
                            self.add_cards_to_hand([card_to_take])
                            return card_to_take
                        # h1 < c < h2
                        if c.value + 1 == h1.value + 2 == h2.value and c.suit == h1.suit == h2.suit:
                            card_to_take = c
                            self.add_cards_to_hand([card_to_take])
                            return card_to_take
                        # h1 < h2 < c
                        if c.value == h1.value + 2 == h2.value + 1 and c.suit == h1.suit == h2.suit:
                            card_to_take = c
                            self.add_cards_to_hand([card_to_take])
                            return card_to_take
        # check whether can be combined as a double
        for h in reversed(self.hand):
            for c in cards:
                if h.value == c.value:
                    card_to_take = c
                    self.add_cards_to_hand([card_to_take])
                    return card_to_take
        # check whether is greater than any card on hand
        for h in reversed(self.hand):
            for c in cards:
                if h.value > c.value:
                    card_to_take = c
                    self.add_cards_to_hand([card_to_take])
                    return card_to_take
        # no card taken, return None
        return card_to_take