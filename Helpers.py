""" A function that returns the total value of a hand """
def get_hand_value(hand):
    return sum(list(map(lambda x: x.value if x.value < 10 else 10, hand)))

"""A  function that shows all the playable plays given a hand"""
def show_plays(hand):
    # trivial sets
    plays = []
    for card in hand:
        plays.append([card])

    # two or more cards of same value
    for i in range (len(hand)):
        #issue and workaround:
        #If we have all four "2" cards, we want to output every possible combination
        #of them, i.e.:
        #[2spades, 2hearts], [2spades,2diamonds], [2spades,2clubs], [2spades,2hearts,2diamonds], etc.
        #
        #We can achieve a hacky workaround by considering all cards except for the first 1, first 2,
        #and first 3 in separate loops
        for k in range(1,4):
            running_same_value_set = [hand[i]]
            for j in range (i + k, len(hand)):
                if running_same_value_set[-1].value == hand[j].value:
                    running_same_value_set.append(hand[j])
                    plays.append(running_same_value_set.copy())
                else:
                    break

    #Consider every card in hand, except the last 2 and except the jokers, as an "anchor card", the first card of a straight
    #TBD - queens and kings can't start? the logic should catch this, however
    for i in range (len(hand) - 2):
        #jokers cannot be part of a straight
        if hand[i].value != 0:
            #form a "consideration hand" starting with the "anchor card"
            straight_considered = [hand[i]]
            #for every card after, if the value is 1 more than previous card, append it to the "consideration hand".
            #remember that as part of sort_value, cards with the same suit are separated from each other by 4, not 1.
            #if the length of the "consideration hand" is 3 or more, add the current entry to the "valid plays" array
            #if the values do not line up, break from this completely and consider a new "anchor card"
            for j in range (i + 1, len(hand)):
                if hand[j].sort_value() == (straight_considered[-1].sort_value() + 4) :
                    straight_considered.append(hand[j])
                    if len(straight_considered) >= 3:
                        plays.append(straight_considered.copy())
                #break, as the current sequence has ended
                elif hand[j].sort_value() > (straight_considered[-1].sort_value() + 4) :
                    break

    return plays
