#SA because as games progress, moves should be more optimized,
#but earlier on a move that does not maximize score at a given step could lead to better results in the future

from Player import Player
from Deck import Deck
import Helpers
import Heuristic.HeuristicHelpers as HeuristicHelpers
import random

"""A Simulated Annealing AI that uses internal temperature to decide plays"""
class SimulatedAnnealingPlayer(Player):
    def __init__(self, id=None):
        super().__init__(id)
        self.intended_card_to_take = None
        self.PENALTY_PER_TURN = HeuristicHelpers.SIMULATED_ANNEALING_PENALTY_PER_TURN

        self.FIXED_RANDOM_VALUE = HeuristicHelpers.SIMULATED_ANNEALING_FIXED_RANDOM_VALUE
        self.RANDOM_FIXED_VALUE = HeuristicHelpers.SIMULATED_ANNEALING_RANDOM_CARD_FIXED_VALUE
        self.RANDOM_INIT_VALUE = HeuristicHelpers.SIMULATED_ANNEALING_RANDOM_CARD_INIT_VALUE

        self.LINEAR_COOLING = HeuristicHelpers.SIMULATED_ANNEALING_LINEAR_COOLING
        self.LINEAR_COOLING_AMOUNT = HeuristicHelpers.SIMULATED_ANNEALING_FIXED_COOLING_VALUE
        self.LINEAR_COOLING_INIT_TEMP = HeuristicHelpers.SIMULATED_ANNEALING_FIXED_INITIAL_TEMPERATURE

        self.temperature = SIMULATED_ANNEALING_FIXED_INITIAL_TEMPERATURE if self.LINEAR_COOLING else 1
        self.turn_count = 0

    def decide_call_yaniv(self, game):
        if Helpers.get_hand_value(self.hand) <= 5:
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
        poss_plays_index = HeuristicHelpers.argsmax(plays_points)

        #check which of those leads to lowest score in future
        poss_scores = []
        for index in poss_plays_index:
            for card in plays[index]:
                next_hand = hand.copy()
                next_hand.remove(card)
                poss_scores.append(self.PENALTY_PER_TURN + self.score(next_hand))

        return min(poss_scores)

    """decide on a new temperature based on turn count and how close other players are to winning"""
    def find_new_temperature(self, game):
        if (self.LINEAR_COOLING):
            self.temperature -= self.LINEAR_COOLING_AMOUNT
            return self.temperature / self.LINEAR_COOLING_INIT_TEMP
        else:
            state = game.get_state(game.player_id)

            #if any player has low number of cards, then game might be over soon, so cool based on lowest number of cards of any player
            min_others_size = min(list(map(lambda hand: len(hand),state['others_hand'])))

            #also consider own hand
            self_score = sum(list(map(lambda c: c.value, self.hand)))

            estimated_turns_remaining = min(int(self_score/5), min_others_size)
            self.temperature = self.turn_count / (self.turn_count + estimated_turns_remaining)

            return self.temperature

    def decide_cards_to_discard(self, game):
        if (self.decide_call_yaniv(game)):
            return []

        possible_takes = game.get_top_discards() #assume is a list of cards
        possible_plays = Helpers.show_plays(self.hand)

        self.turn_count += 1
        temperature = self.find_new_temperature(game)

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

        scores.sort(key=lambda x:x[1])
        chosen_play, chosen_score = random.choice(scores[0 : max(int(len(scores) * temperature),1)])
        poss_scores.append((None, chosen_play, chosen_score))

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

            scores.sort(key=lambda x:x[1])
            chosen_play, chosen_score = random.choice(scores[0 : max(int(len(scores) * temperature),1)])
            poss_scores.append((poss_take, chosen_play, chosen_score))

        #choose play based on temperature
        poss_scores.sort(key=lambda x:x[2])
        chosen_take, chosen_play, chosen_score = random.choice(poss_scores[0 : max(int(len(poss_scores) * temperature),1)])

        self.intended_card_to_take = chosen_take
        return chosen_play

    def decide_cards_to_draw(self, game):
        if self.intended_card_to_take == None:
            return "unseen_pile", None
        else:
            return "discard_pile", self.intended_card_to_take
