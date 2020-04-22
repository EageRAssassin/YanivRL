from Player import Player
from Deck import Deck
import Helpers
import Heuristic.HeuristicHelpers as HeuristicHelpers

"""A simple Hill Climb AI that tries to minimize its own hand every turn"""
class HillClimbPlayer(Player):
    def __init__(self, id=None):
        super().__init__(id)
        self.intended_card_to_take = None
        self.PENALTY_PER_TURN = HeuristicHelpers.HILL_CLIMB_PENALTY_PER_TURN

    def decide_call_yaniv(self, game):
        if self.get_hand_value() <= 5:
            return True
        return False

    """ Assigns a score to the hand, lower scores are better"""
    def score(self, hand):
        #find total number of points in hand, cards above 10 are worth 10 points
        points = sum(list(map(lambda x: x.value if x.value < 10 else 10, hand)))

        #find minimum turns necessary to get below 5 points
        if (points) <= 5:
            return points

        plays = Helpers.show_plays(hand)
        plays_points = list(map(lambda play: sum(list(map(lambda x: x.value if x.value < 10 else 10, play))), plays))

        #do a play that removes most points
        poss_plays_index = HeuristicHelpers.argsmax(play_points)

        #check which of those leads to lowest score in future
        poss_scores = []
        for index in poss_plays_index:
            for card in plays[index]:
                next_hand = hand.copy().remove(card)
                poss_scores.append(self.PENALTY_PER_TURN + self.score(next_hand))

        return min(poss_scores)

    def decide_cards_to_discard(self, game):
        possible_takes = game.get_top_discard() #assume is a list of cards
        possible_plays = Helpers.show_plays(self.hand)

        #a list of tuples of (card_to_take, best play, score assuming card is taken and best play is made)
        poss_scores = []

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

        #take card from draw pile
        poss_scores.append(None, self.PENALTY_PER_TURN + self.score(next_hand))
        scores = []

        #score each possible discard hand
        for play in possible_plays:
            next_hand = self.hand.copy()
            for card in play:
                next_hand.remove(card)
            next_hand.append(poss_take)
            scores.append((play, score(next_hand, self.PENALTY_PER_TURN)))

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

#
#
# #Test Section
# hand = Deck().get_cards()
#
# len(hand)
# Helpers.get_hand_value(hand)
# 340/54
#
#
# player = HillClimbPlayer("HCP")
#
# player.add_cards_to_hand(hand)
#
# player.hand
#
# plays = player.show_plays()
#
# plays
#
# play_points = list(map(lambda play: sum(list(map(lambda x: x.value if x.value < 10 else 10, play))), plays))
#
# play_points
#
#
# argsmax(play_points)
#
# plays[]
# max(play_points)
#
# hand
#
# for card in plays[argmax(play_points)]:
#     hand.remove(card)
#
#
# player.score(player.hand)
