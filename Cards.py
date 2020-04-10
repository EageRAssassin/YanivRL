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

    def get_str(self):
        return self.value + '-' + self.suit

# c = Card(12, "Clubs")
# print(c)
