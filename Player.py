import random
import Cards
import math


# class for Players that all Players should inherit from
class Player:
    def __init__(self):
        self.hand = []

    def add_cards_to_hand(self, cards):
        """A  function that receives card and organize on his hands"""
        for card in cards:
            # if there is no card on hand or the card is greater than cards in hand
            if len(self.hand) == 0 or self.hand[-1].value <= card.value:
                self.hand.append(card)
            else:
                # find the first card that is greater or equal than the card
                # append before it
                for i in range(len(self.hand)):
                    if self.hand[i].value >= card.value:
                        self.hand.insert(i, card)
                        break

    def show_plays(self):
        """A  function that shows all the playable strategies"""
        # choose in random order
        plays = []
        for card in self.hand:
            plays.append([card])
        # find the choices for a pair
        for i in range(len(self.hand) - 1):
            if self.hand[i].value == self.hand[i + 1].value:
                plays.append([self.hand[i], self.hand[i + 1]])
            # the choices for a straight
        for i in range(len(self.hand) - 2):
            for j in range(i, len(self.hand) - 1):
                for k in range(j, len(self.hand)):
                    if self.hand[i].value + 2 == self.hand[j].value + 1 == self.hand[k].value \
                            and self.hand[i].suit == self.hand[j].suit == self.hand[k].suit:
                        plays.append([self.hand[i], self.hand[j], self.hand[k]])
        return plays

    def play_from_hand_random(self):
        """A function that chooses to play randomly from all the playable strategies"""
        # w
        if self.yaniv():
            return []
        plays = self.show_plays()
        # there are (choices) random choices
        # we pick a random number from 0 to choice
        choice = random.uniform(0, len(plays))
        return plays[math.floor(choice)]

    def play_optimally(self):
        """A function that chooses to play optimally by choosing the last option in the plays"""
        if self.yaniv():
            return []
        plays = self.show_plays()
        return plays[-1]

    def take_from_discard_random(self, cards):
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

    def show_cards(self):
        return self.hand

    def yaniv(self):
        sum = 0
        for card in self.hand:
            sum += card.value
        return sum <= 5

# testing player functionality
p = Player()
cards = []
cards.append(Cards.Card(3, "Clubs"))
cards.append(Cards.Card(2, "Clubs"))
cards.append(Cards.Card(3, "Diamonds"))
cards.append(Cards.Card(2, "Diamonds"))
cards.append(Cards.Card(1, "Diamonds"))
cards.append(Cards.Card(3, "Spades"))
cards.append(Cards.Card(2, "Spades"))
p.add_cards_to_hand(cards)
print("show_cards", p.show_cards())
print("show_plays", p.show_plays())

p = Player()
cards = []
cards.append(Cards.Card(5, "Clubs"))
cards.append(Cards.Card(4, "Clubs"))
cards.append(Cards.Card(3, "Diamonds"))
cards.append(Cards.Card(2, "Diamonds"))
p.add_cards_to_hand(cards)
print("show_cards", p.show_cards())
print("show_plays", p.show_plays())
print(p.take_from_discard_random([Cards.Card(3, "Diamonds"), Cards.Card(3, "Clubs")]))
print(p.take_from_discard_random([Cards.Card(2, "Diamonds"), Cards.Card(5, "Clubs")]))
print(p.take_from_discard_random([Cards.Card(6, "Diamonds")]))
print(p.take_from_discard_random([Cards.Card(6, "Clubs")]))


p = Player()
cards = []
cards.append(Cards.Card(1, "Clubs"))
cards.append(Cards.Card(1, "Diamonds"))
cards.append(Cards.Card(2, "Clubs"))
cards.append(Cards.Card(0, ""))
p.add_cards_to_hand(cards)
print("play_optimally", p.play_optimally())
