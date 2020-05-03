from Player import Player
from Deck import Deck
import Helpers
import Heuristic.HeuristicHelpers as HeuristicHelpers


#ditch hand if others are winning
#minimize next player given what we know of his hand

# max(player) -> min all others
"""A Minimax AI"""
class MinimaxPlayer(Player):
    def __init__(self, id=None):
        super().__init__(id)
        self.intended_card_to_take = None

        self.MINIMAX_DEPTH = HeuristicHelpers.MINIMAX_DEPTH
        self.PENALTY_PER_TURN = HeuristicHelpers.MINIMAX_PENALTY_PER_TURN
        self.FIXED_RANDOM_VALUE = HeuristicHelpers.MINIMAX_FIXED_RANDOM_VALUE
        self.RANDOM_FIXED_VALUE = HeuristicHelpers.MINIMAX_RANDOM_CARD_FIXED_VALUE
        self.RANDOM_INIT_VALUE = HeuristicHelpers.MINIMAX_RANDOM_CARD_INIT_VALUE

    def decide_call_yaniv(self, game):
        return Helpers.get_hand_value(self.hand) <= 5

    """ Assigns a score to the hand, lower scores are better"""
    def score(self, hand):
        #find total number of points in hand, cards above 10 are worth 10 points
        points = Helpers.get_hand_value(hand)

        #find minimum turns necessary to get below 5 points
        if (points) <= 5:
            return points

        plays = Helpers.show_plays(hand)
        plays_points = list(map(lambda play: Helpers.get_hand_value(play), plays))

        #do a play that removes most points
        poss_plays_index = HeuristicHelpers.argsmax(plays_points)

        #check which of those leads to lowest score in future
        poss_scores = []
        for index in poss_plays_index:
            for card in plays[index]:
                next_hand = hand.copy()
                next_hand.remove(card)
                poss_scores.append(self.PENALTY_PER_TURN + self.score(next_hand))

        return min(poss_scores)

    """ assigns a value to hands with unknown elements"""
    def get_unknown_hand_value(self, hand):
        val = 0

        known_cards = []
        for card in hand:
            if card == None:
                val += self.PENALTY_PER_TURN / 2 + self.RANDOM_FIXED_VALUE
            else:
                known_cards.append(card)

        val += self.score(known_cards)

        return val

    """
    gets the optimal play using the minimax algorithm
    returns a (play, score) tuple at every depth
    """
    def minimax_play(self, self_hand, others_hands, num_players, depth):
        if (depth == self.MINIMAX_DEPTH):
            if (depth % num_players == 0):
                return[None, self.score(self_hand)]
            else:
                return [None, self.get_unknown_hand_value(others_hands[depth % num_players - 1])]

        #if is self, maximize score, else minimize score
        if (depth % num_players == 0):

            return 0
        else:




    def decide_cards_to_discard(self, game):
        if (self.decide_call_yaniv(game)):
            return []

        num_players = game.get_num_players()



        possible_takes = game.get_top_discards() #assume is a list of cards
        possible_plays = Helpers.show_plays(self.hand)

        #a list of tuples of (card_to_take, best play, score assuming card is taken and best play is made)
        poss_scores = []

        #take card from draw pile
        scores = []

        #score each possible discard hand
        for play in possible_plays:
            next_hand = self.hand.copy()
            for card in play:
                next_hand.remove(card)
            if self.FIXED_RANDOM_VALUE:
                random_card_value = self.RANDOM_FIXED_VALUE
            else:
                disc_score = self.score(self.hand) - sum([c.value for c in play])
                random_card_value = int(self.RANDOM_INIT_VALUE * disc_score /70)
            scores.append((play, self.score(next_hand) + random_card_value))


        best_play, best_score = min(scores,key=lambda x:x[1])
        poss_scores.append((None, best_play, best_score))

        #take a card from discard
        for poss_take in possible_takes:
            scores = []

            #score each possible discard hand
            for play in possible_plays:
                next_hand = self.hand.copy()
                for card in play:
                    next_hand.remove(card)
                next_hand.append(poss_take)
                scores.append((play, self.score(next_hand)))

            best_play, best_score = min(scores,key=lambda x:x[1])
            poss_scores.append((poss_take, best_play, best_score))

        #choose play with minimum score
        best_take, best_play, best_score = min(poss_scores,key=lambda x:x[2])

        self.intended_card_to_take = best_take
        return best_play

    def decide_cards_to_draw(self, game):
        if self.intended_card_to_take == None:
            return "unseen_pile", None
        else:
            return "discard_pile", self.intended_card_to_take

    def set_parameters(self, ppt, frv, rfv, riv):
        self.PENALTY_PER_TURN = ppt
        self.FIXED_RANDOM_VALUE = frv
        self.RANDOM_FIXED_VALUE = rfv
        self.RANDOM_INIT_VALUE = riv
