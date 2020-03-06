suits = ['hearts', 'diamonds', 'spades', 'clubs']

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__ (self):
        table = {
            11: "Jack",
            12: "Queen",
            13: "King",
            None: "Joker"}

        return "Joker" if self.value = None else table.get(self.value,str(self.value)) + " of " + self.suit