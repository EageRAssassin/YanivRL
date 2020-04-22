import random
import Cards
import math
import Helpers


# class for Players that all Players should inherit from
class Player:
    def __init__(self, id=None):
        self.id = id
        self.hand = []

    def __str__(self):
        return str(self.id)

    def extract_cards(self, cards):
        for card in cards:
            self.hand.remove(card)

    def add_cards_to_hand(self, cards):
        """A  function that receives card and organize on his hands"""
        for card in cards:
            self.hand.append(card)
        self.hand.sort(key=lambda c: c.sort_value())

    def show_plays(self):
        plays = Helpers.show_plays(self.hand)
        if self.yaniv():
            plays += []
        return plays

    def play_optimally(self):
        """A function that chooses to play optimally by choosing the last option in the plays"""
        if self.yaniv():
            return []
        plays = self.show_plays()
        return plays[-1]

    def show_cards(self):
        return self.hand

    def yaniv(self):
        return self.get_hand_value() <= 5

    def get_hand_value(self):
        return Helpers.get_hand_value(self.hand)

    def decide_cards_to_draw(self, game):
        '''
            Decide which pile the player wish to draw card(s) from,
            and which cards he wish to draw.

            Returns pile (string rep), a card
        '''
        raise NotImplementedError

    def decide_cards_to_discard(self, game):
        '''
            Decide which cards the player wish to discard.

            Returns a list of card
        '''
        raise NotImplementedError

    def decide_call_yaniv(self, game):
        '''
            Returns True if the player decides to call Yaniv.
        '''
        raise NotImplementedError

# testing player functionality
# p = Player()
# cards = []
# cards.append(Cards.Card(3, "Clubs"))
# cards.append(Cards.Card(2, "Clubs"))
# cards.append(Cards.Card(3, "Diamonds"))
# cards.append(Cards.Card(2, "Diamonds"))
# cards.append(Cards.Card(1, "Diamonds"))
# cards.append(Cards.Card(3, "Spades"))
# cards.append(Cards.Card(2, "Spades"))
# p.add_cards_to_hand(cards)
# print("show_cards", p.show_cards())
# print("show_plays", p.show_plays())

# p = Player()
# cards = []
# cards.append(Cards.Card(5, "Clubs"))
# cards.append(Cards.Card(4, "Clubs"))
# cards.append(Cards.Card(3, "Diamonds"))
# cards.append(Cards.Card(2, "Diamonds"))
# p.add_cards_to_hand(cards)
# print("show_cards", p.show_cards())
# print("show_plays", p.show_plays())
# print(p.take_from_discard_random([Cards.Card(3, "Diamonds"), Cards.Card(3, "Clubs")]))
# print(p.take_from_discard_random([Cards.Card(2, "Diamonds"), Cards.Card(5, "Clubs")]))
# print(p.take_from_discard_random([Cards.Card(6, "Diamonds")]))
# print(p.take_from_discard_random([Cards.Card(6, "Clubs")]))


# p = Player()
# cards = []
# cards.append(Cards.Card(1, "Clubs"))
# cards.append(Cards.Card(1, "Diamonds"))
# cards.append(Cards.Card(2, "Clubs"))
# cards.append(Cards.Card(0, ""))
# p.add_cards_to_hand(cards)
# print("play_optimally", p.play_optimally())
