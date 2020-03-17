from enum import Enum

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return str(self.value) + " of " + self.suit
