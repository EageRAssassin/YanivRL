import random
import Cards
import math


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
        """A  function that shows all the playable strategies"""
        # trivial sets
        plays = []
        for card in self.hand:
            plays.append([card])

        # two or more cards of same value
        running_same_value_set = [self.hand[0]]
        for card in self.hand[1:]:
            if running_same_value_set[-1].value == card.value:
                running_same_value_set.append(card)
            elif len(running_same_value_set) > 1:
                plays.append(running_same_value_set)
                running_same_value_set = [card]
            else:
                running_same_value_set = [card]
        if len(running_same_value_set) > 1:
            plays.append(running_same_value_set)

        #Consider every card in hand, except the last 2 and except the jokers, as an "anchor card", the first card of a straight
        #TBD - queens and kings can't start? the logic should catch this, however
        for i in range (len(self.hand) - 2):
            #jokers cannot be part of a straight
            if self.hand[i].value != 0:
                #form a "consideration hand" starting with the "anchor card"
                straight_considered = [self.hand[i]]
                #for every card after, if the value is 1 more than previous card, append it to the "consideration hand".
                #remember that as part of sort_value, cards with the same suit are separated from each other by 4, not 1.
                #if the length of the "consideration hand" is 3 or more, add the current entry to the "valid plays" array
                #if the values do not line up, break from this completely and consider a new "anchor card"
                for j in range (len(self.hand) - i + 1):
                    if sort_value(self.hand[j].value) == (sort_value(straight_considered[-1].value) + 4) :
                        straight_considered.append(self.hand[j])
                        if len(straight_considered) >= 3:
                            # CHECK: does this append a copy or the actual array? Will future edits overwrite the hand?
                            plays.append(straight_considered)
                    #break, as the current sequence has ended
                    elif sort_value(self.hand[j].value) > (sort_value(straight_considered[-1].value) + 4) :
                        break

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
        sum = 0
        for card in self.hand:
            sum += card.value
        return sum

    def decide_cards_to_draw(self, game):
        '''
            Decide which pile the player wish to draw card(s) from,
            and which cards he wish to draw.

            Returns pile (string rep), a list of card
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
