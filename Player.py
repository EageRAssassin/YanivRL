# class for Players that all Players should inherit from

class Player:
    def __init__(self, init_gamestate):
        self.cards = init_gamestate.cards
        self.discards = init_gamestate.discards
        """etc"""
    
    #TODO:: add args after GameEngine exists
    #def play_from_hand("""args"""):
    #def take_discard("""args"""):