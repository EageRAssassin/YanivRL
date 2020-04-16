import numpy as np
from Cards import Card

# Card combination: Use for action decoding

suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
double_combination = [["Clubs", "Diamonds"], ["Clubs", "Hearts"], ["Clubs", "Spades"], ["Diamonds", "Hearts"],
                      ["Diamonds", "Spades"], ["Hearts", "Spades"]]
triple_combination = [["Clubs", "Diamonds", "Hearts"], ["Clubs", "Diamonds", "Spades"], ["Clubs", "Hearts", "Spades"],
                      ["Diamonds", "Hearts", "Spades"]]

# initialize the one-hot dictionary for cards
# NOT USED FOR NOW
card_encoding_dict = {}
num = 0
for s in suits:
    for v in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
        card = s+"-"+v
        card_encoding_dict[card] = num
        num += 1
# encode the two joker
card_encoding_dict['01'] = num
num += 1
card_encoding_dict['02'] = num
# NOT USED FOR NOW


def encode_cards(cards):
    # encode the cards into a
    cards_list = []
    for c in cards:
        cards_list.append(c.get_str())
    return cards_list


def encode_action_discard(action):
    """ Return action id of the action from the player
        returned action id is a integer ranging from 0 to 347
    """
    return 0


def decode_action_discard(action):
    """ Return the cards to be discarded from the action
        Action is a integer ranging from 0 to 347
    """
    discard = []
    # find the cards behind the action number
    # 52(single)+78(double)+52(triple)+13(quadruple)+44(staight3)+40(staight4)+36(staight5)+32(6)
    # card ranges from 1 to 13, suit ranges from CDHS
    if action <= 52:
        # single
        action -= 1
        rank = action % 13 + 1
        suit = suits[int(action/13)]
        discard = [Card(rank, suit)]
    elif action <= 130:
        # double
        action -= 53
        rank = action % 13 + 1
        suit1 = double_combination[int(action/13)][0]
        suit2 = double_combination[int(action/13)][1]
        discard = [Card(rank, suit1), Card(rank, suit2)]
    elif action <= 182:
        # triple
        action -= 131
        rank = action % 13 + 1
        suit1 = triple_combination[int(action/13)][0]
        suit2 = triple_combination[int(action/13)][1]
        suit3 = triple_combination[int(action/13)][2]
        discard = [Card(rank, suit1), Card(rank, suit2), Card(rank, suit3)]
    elif action <= 195:
        # quadruple
        action -= 183
        rank = action + 1
        discard = [Card(rank, "Clubs"), Card(rank, "Diamonds"), Card(rank, "Hearts"), Card(rank, "Spades")]
    elif action <= 239:
        # straight of 3
        action -= 196
        suit = suits[int(action/11)]
        rank = action % 11 + 1
        discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit)]
    elif action <= 279:
        # straight of 4
        action -= 240
        suit = suits[int(action/10)]
        rank = action % 10 + 1
        discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit), Card(rank + 3, suit)]
    elif action <= 315:
        # straight of 5
        action -= 280
        suit = suits[int(action/9)]
        rank = action % 9 + 1
        discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit), Card(rank + 3, suit), Card(rank + 4, suit)]
    elif action <= 347:
        # straight of 6
        action -= 316
        suit = suits[int(action/8)]
        rank = action % 8 + 1
        discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit), Card(rank + 3, suit), Card(rank + 4, suit), Card(rank + 5, suit)]
    return discard


# discard_cards = decode_action_discard(347)
# print(discard_cards)

cards = [Card(12, "Clubs"), Card(0, ''), Card(0, ''), Card(2, 'Hearts')]
encoding = encode_cards(cards)
print(encoding)
