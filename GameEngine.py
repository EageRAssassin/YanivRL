from Cards import Card, Suits
from numpy.random import shuffle

class GameEngine:
    """Initializes a new game of Yaniv"""
    def __init__(self, **players):
        """init players"""
        self.players = [player for player in players]
        self.current_player = 0

        """init cards"""
        #cards from draw pile goes to players hands
        self.draw_pile = [Card(val,suit) for val in range(1, 14) for suit in Suits]
        self.draw_pile.append(Card(None, None))
        self.draw_pile.append(Card(None, None))
        shuffle(self.draw_pile)

        #current play is top of discard pile, where player can take cards
        #plays made by players goes to the current play
        #which pushes the existing current play to discard
        self.current_play = []
        self.discard_pile = []

        """init game vars"""
        self.game_over = False
        self.turn_number = 0

        """init player hands"""
        self.hands = [[draw_pile.pop() for _ in range(7)] for player in players]

        for i in range(len(players)):
            players[i].add_cards_to_hand(self.hands[i])

        """init top of discard pile"""
        self.current_play = [draw_pile.pop()]


    def take_turn(self):
        pass

    def start_game(self):
        pass
