
def cards2str(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of Card objects

    Returns:
        string: string representation of cards
    '''
    response = ''
    for card in cards:
        if card.rank == '':
            response += card.suit[0]
        else:
            response += card.rank
    return response


# def encode_cards(plane, cards):
#     ''' Encode cards and represerve it into plane.
#
#     Args:
#         cards (list or str): list or str of cards, every entry is a
#     character of solo representation of card
#     '''
#     if not cards:
#         return None
#     layer = 1
#     if len(cards) == 1:
#         rank = CARD_RANK_STR.index(cards[0])
#         plane[layer][rank] = 1
#         plane[0][rank] = 0
#     else:
#         for index, card in enumerate(cards):
#             if index == 0:
#                 continue
#             if card == cards[index-1]:
#                 layer += 1
#             else:
#                 rank = CARD_RANK_STR.index(cards[index-1])
#                 plane[layer][rank] = 1
#                 layer = 1
#                 plane[0][rank] = 0
#         rank = CARD_RANK_STR.index(cards[-1])
#         plane[layer][rank] = 1
#         plane[0][rank] = 0