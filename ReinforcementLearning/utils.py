import numpy as np
from Cards import Card

# Card combination: Use for action decoding

suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
double_combination = [["Clubs", "Diamonds"], ["Clubs", "Hearts"], ["Clubs", "Spades"], ["Diamonds", "Hearts"],
                      ["Diamonds", "Spades"], ["Hearts", "Spades"]]
triple_combination = [["Clubs", "Diamonds", "Hearts"], ["Clubs", "Diamonds", "Spades"], ["Clubs", "Hearts", "Spades"],
                      ["Diamonds", "Hearts", "Spades"]]

# Initialize the one-hot dictionary for cards
card_encoding_dict = {}
num = 0
for s in suits:
    for v in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']:
        card = v+"-"+s
        card_encoding_dict[card] = num
        num += 1
# encode the two joker
card_encoding_dict['01'] = num
num += 1
card_encoding_dict['02'] = num


def encode_cards(cards_str):
    """ Encode cards and save it into plane. """
    plane = np.zeros(54, dtype=int)
    joker_counter = 0
    for card_str in cards_str:
        if card_str == '0' and joker_counter == 0:
            # handle the first joker situation
            joker_counter = 1
            index = card_encoding_dict['01']
            plane[index] = 1
        elif card_str == '0' and joker_counter == 1:
            # handle the second joker situation
            index = card_encoding_dict['02']
            plane[index] = 1
        else:
            index = card_encoding_dict[card_str]
            plane[index] = 1
    return plane


def cards_to_str(cards):
    """ Encode cards into a list of string """
    cards_list = []
    for c in cards:
        cards_list.append(c.get_str())
    return cards_list


def encode_action_discard(play_list):
    """ Return action id of the action from the player
        returned action id is a integer ranging from 0 to 347
    """
    action_id_list = []
    for play in play_list:
        # encode the cards in plays into individual action id
        # TODO if YANIV is included in the plays
        # TODO Does the straight plays from player always sorted?

        cards_have_same_value = True
        for card in play:
            if card.value != play[0].value:
                cards_have_same_value = False

        action = 0
        if len(play) == 1:
            # single
            suit_num = suits.index(play[0].suit)
            action = suit_num * 13 + card.value - 1
            action += 1
        elif len(play) == 2 and cards_have_same_value:
            # double
            suits_temp = [play[0].suit, play[1].suit]
            suits_temp.sort()
            suit_num = double_combination.index(suits_temp)
            action = suit_num * 13 + card.value - 1
            action += 53
        elif len(play) == 3 and cards_have_same_value:
            # triple
            suits_temp = [play[0].suit, play[1].suit, play[2].suit]
            suits_temp.sort()
            suit_num = triple_combination.index(suits_temp)
            action = suit_num * 13 + card.value - 1
            action += 131
        elif len(play) == 4 and cards_have_same_value:
            # quadruple
            action = play[0].value - 1
            action += 183
        elif len(play) == 3:
            # straight of 3
            suit_num = suits.index(play[0].suit)
            action = suit_num * 11 + play[0].value - 1
            action += 196
        elif len(play) == 4:
            # straight of 4
            suit_num = suits.index(play[0].suit)
            action = suit_num * 10 + play[0].value - 1
            action += 240
        elif len(play) == 5:
            # straight of 5
            suit_num = suits.index(play[0].suit)
            action = suit_num * 9 + play[0].value - 1
            action += 280
        elif len(play) == 6:
            # straight of 6
            suit_num = suits.index(play[0].suit)
            action = suit_num * 8 + play[0].value - 1
            action += 316
        action_id_list.append(action)
    return action_id_list


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


""" Convert cards to string test """
# cards = [Card(12, "Clubs"), Card(0, ''), Card(0, ''), Card(2, 'Hearts')]
# cards_str_temp = cards_to_str(cards)
# print(cards_str_temp)

""" Encode Cards test """
# cards_encoding = encode_cards(cards_str_temp)
# print(cards_encoding)

""" General Encoding and Decoding Cards test """
# for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
#     for rank in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
#         cards = [Card(rank, suit)]
#         cards_str_temp = cards_to_str(cards)
#         cards_encoding = encode_cards(cards_str_temp)
#         print(cards_encoding)

""" Decode action test """
# action_id = 185
# print(action_id)
# discard_cards = decode_action_discard(action_id)
# print(discard_cards)

""" Encode plays test """
# plays = [discard_cards]
# actions = encode_action_discard(plays)
# print(actions)

""" General Encoding and Decoding action test """
# for i in range(195):
#     discard_cards = decode_action_discard(i)
#     plays = [discard_cards]
#     actions = encode_action_discard(plays)
#     if i != actions[0]:
#         print(i)
