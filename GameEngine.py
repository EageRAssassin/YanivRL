from Cards import Card
from numpy.random import shuffle
import math
import random


class GameEngine:
    """Initializes a new game of Yaniv"""

    def __init__(self, **players):
        """init players"""
        self.players = [player for player in players]
        self.current_player = 0

        """init cards"""
        # cards from draw pile goes to players hands
        Suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        self.draw_pile = [Card(val, suit) for val in range(1, 14) for suit in Suits]
        self.draw_pile.append(Card(None, None))
        self.draw_pile.append(Card(None, None))
        shuffle(self.draw_pile)

        # current play is top of discard pile, where player can take cards
        # plays made by players goes to the current play
        # which pushes the existing current play to discard
        self.current_play = []
        self.discard_pile = []

        """init game vars"""
        self.game_over = False
        self.turn_number = 0

        """init player hands"""
        self.hands = [[self.draw_pile.pop() for _ in range(7)] for player in players]

        for i in range(len(players)):
            players[i].add_cards_to_hand(self.hands[i])

        """init top of discard pile"""
        self.current_play = [self.draw_pile.pop()]

    # def take_turn(self):

    def start_game(self):
        prev_discard_cards = []
        discard_cards = []
        while not self.game_over:
            for player in self.players:
                discard_cards = player.play_optimally()
                # the player calls Yaniv
                if discard_cards == []:
                    print(player, "calls Yaniv")
                    self.game_over = True
                    break
                take_discard = player.take_from_discard_random(prev_discard_cards)
                # the player want to choose randomly from the card pool
                if take_discard is None:
                    random_card = self.take_random_from_card_pool()
                    player.add_cards_to_hand(random_card)
                    self.draw_pile.remove(random_card)
                else:
                    self.draw_pile.append(prev_discard_cards)
                    self.draw_pile.remove(take_discard)
                prev_discard_cards = discard_cards

    def take_random_from_card_pool(self):
        choice = random.uniform(0, len(self.draw_pile))
        return self.draw_pile[math.floor(choice)]
