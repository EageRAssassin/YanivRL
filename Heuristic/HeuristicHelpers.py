import numpy as np

def argsmax(list):
    return np.argwhere(list == np.amax(list)).flatten().tolist()

""" Assigns a score to the hand, lower scores are better"""
def hill_climb_score(hand, penalty_per_turn = 15):
    #find total number of points in hand, cards above 10 are worth 10 points
    points = sum(list(map(lambda x: x.value if x.value < 10 else 10, hand)))

    #find minimum turns necessary to get below 5 points
    if (points) <= 5:
        return points

    plays = Helpers.show_plays(hand)
    plays_points = list(map(lambda play: sum(list(map(lambda x: x.value if x.value < 10 else 10, play))), plays))

    #do a play that removes most points
    poss_plays_index = argsmax(play_points)

    poss_scores = []
    for index in poss_plays_index:
        for card in plays[index]:
            next_hand = hand.copy().remove(card)
            poss_scores.append(PENALTY_PER_TURN + hill_climb_score(next_hand, penalty_per_turn))

    return min(poss_scores)
