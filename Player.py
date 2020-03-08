# class for Players that all Players should inherit from

class Player:
    def __init__(self):
        self.hand = []
        """etc"""

    def add_cards_to_hand(self, cards):
        for card in cards:
            self.hand.append(card)

    #TODO:: add args after GameEngine exists
    #def play_from_hand("""args"""):
    #def take_from_discard("""args"""):
