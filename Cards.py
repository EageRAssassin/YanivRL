# Suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        if self.value == 0:
            return "Joker"
        if self.value == 11:
            return "Knight" + " of " + self.suit
        if self.value == 12:
            return "Queen" + " of " + self.suit
        if self.value == 13:
            return "King" + " of " + self.suit
        return str(self.value) + " of " + self.suit

    def __eq__(self, other):
        if isinstance(other, Card):
            if self.value == 0:
                return other.value == 0
            return self.value == other.value and self.suit == other.suit
        return False

    def get_str(self):
        if self.value == 0:
            return '0'
        return str(self.value) + '-' + self.suit

    """ used to sort card by value, then suit"""
    def sort_value(self):
        if self.value == 0:
            return 0
        if self.suit == "Spades":
            return 4 * self.value
        if self.suit == "Hearts":
            return 4 * self.value + 1
        if self.suit == "Diamonds":
            return 4 * self.value + 2
        if self.suit == "Clubs":
            return 4 * self.value + 3


# c = Card(12, "Clubs")
# print(c)
