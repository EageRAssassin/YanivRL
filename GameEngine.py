from Cards import Card
from Deck import Deck
from numpy.random import shuffle
import math
import random
from BasePlayer import BasePlayer
from RandomPlayer import RandomPlayer


class GameEngine:
    """Initializes a new game of Yaniv"""

    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    double_combination = [["Clubs", "Diamonds"], ["Clubs", "Hearts"], ["Clubs", "Spades"], ["Diamonds", "Hearts"],
                          ["Diamonds", "Spades"], ["Hearts", "Spades"]]
    triple_combination = [["Clubs", "Diamonds", "Hearts"], ["Clubs", "Diamonds", "Spades"], ["Clubs", "Hearts", "Spades"],
                          ["Diamonds", "Hearts", "Spades"]]

    def __init__(self, players):

        """init cards"""
        self.deck = Deck()
        self.players = players
        self.player_id = 0
        """init game vars"""
        self.game_over = False
        self.turn_number = 0

        # """init player hands"""
        # self.hands = [[self.draw_pile.pop() for _ in range(7)] for player in players]

        # for i in range(len(players)):
        #     players[i].add_cards_to_hand(self.hands[i])

        # """init top of discard pile"""
        # self.current_play = [self.draw_pile.pop()]

    def get_top_discard(self):
        return self.deck.get_top_discard()

    def get_top_card(self):
        return self.deck.get_top_card()

    def play_games(self, num_games):
        for i in range(num_games):
            self.deck = Deck()
            self.deal_card()
            self.game_loop()

    def deal_card(self):
        for player in self.players:
            cards = [self.deck.draw_top_card() for _ in range(7)]
            player.add_cards_to_hand(cards)

    def game_loop(self, max_round=100):
        round_cnt = 0        
        while round_cnt < max_round:
            print("======== Round " + str(round_cnt) + " =========")
            for player in self.players:
                print("----- Current player :" + str(player) + "-------")
                if player.decide_call_yaniv(self):
                    print(player, "calls Yaniv")
                    return player, self.get_players_scores(player)
                
                ''' Discard phase '''
                discard_cards = player.decide_cards_to_discard(self)
                print("Player discards : ", [c for c in discard_cards])
                player.extract_cards(discard_cards)
                self.deck.discard(discard_cards)

                ''' Draw phase '''
                pile_to_draw_from, cards = player.decide_cards_to_draw(self)
                if pile_to_draw_from == "discard_pile" :
                    discard_top = self.deck.draw_top_discard()
                    player.add_cards_to_hand([discard_top])
                elif pile_to_draw_from == "unseen_pile":
                    card = self.deck.draw_top_card()
                    player.add_cards_to_hand([card])
                print("Player draws from : ", pile_to_draw_from)

                round_cnt += 1
                # the player want to choose randomly from the card pool
                # if take_discard is None:
                #     card = self.deck.draw_top_card()
                #     player.add_cards_to_hand(card)
                # else:
                #     player.add_cards_to_hand(take_discard)
                #     
                #     self.draw_pile.append(prev_discard_cards)
                #     self.draw_pile.remove(take_discard)
                # prev_discard_cards = discard_cards        

    def step(self, action):
        """ Perform one step for the game for DQN """
        # select player
        player = self.players[self.current_player_id]

        # check action 0 -- player calls yaniv
        if action == 0:
            game_over = True
            self.player_id = (self.player_id + 1) % len(self.players)
            state = self.get_state(self.player_id)
            return player, state

        ''' Discard phase '''
        discard_cards = self.decode_action_discard(action)

        # discard_cards = player.decide_cards_to_discard()
        player.extract_cards(discard_cards)
        self.deck.discard(discard_cards)

        ''' Draw phase '''
        pile_to_draw_from, cards = player.decide_cards_to_draw()
        if pile_to_draw_from == "discard_pile":
            discard_top = self.deck.draw_top_discard()
            player.add_cards_to_hand([discard_top])
        elif pile_to_draw_from == "unseen_pile":
            card = self.deck.draw_top_card()
            player.add_cards_to_hand([card])
        print("Player draws from : ", pile_to_draw_from)

        self.turn_number += 1
        self.player_id = (self.player_id + 1) % len(self.players)
        # get next state
        state = self.get_state(self.player_id)
        self.state = state
        return state, self.player_id

    def get_players_scores(self, yaniv_caller):
        scores_dict = {}
        for player in self.players:
            if player is yaniv_caller:
                    scores_dict[player.id] = 0
            else:
                scores_dict[player.id] = player.get_hand_value()
        return scores_dict

    def get_state(self, player_id):
        ''' Return player's state for DQN

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        player = self.players[player_id]

        state = {}
        state['deck'] = self.deck.get_cards()
        state['discards'] = self.deck.get_discards()
        state['self'] = self.player_id
        state['current_hand'] = cards2str(player.show_cards())
        # state['others_hand'] = others_hands
        state['actions'] = player.show_plays()
        # example of state
        # {
        #     'deck': '3333444455556666777788889999TTTTJJJJQQQQKKKKAAAA2222BR',
        #     'discards': 'TQA',
        #     'self': 2,
        #     'played_cards': ['6', '8', '8', 'Q', 'K', 'K', 'K', '2', '2', '2'],
        #     'others_hand': '333444555678899TTTJJJQQAA2R',
        #     'current_hand': '3456677799TJQKAAB',
        #     'actions': ['pass', 'K', 'A', 'B']
        # }
        return state

    def is_over(self):
        return self.game_over

    def get_payoff(self):
        return -self.turn_number

    def decode_action_discard(self, action):
        """ Return the cards to be discarded from the action """
        discard = []
        # find the cards behind the action number
        # 52(single)+78(double)+52(triple)+13(quadruple)+44(staight3)+40(staight4)+36(staight5)+32(6)
        # card ranges from 1 to 13, suit ranges from CDHS
        if action <= 52:
            # single
            action -= 1
            rank = action % 13 + 1
            suit = self.suits[int(action/13)]
            discard = [Card(rank, suit)]
        elif action <= 130:
            # double
            action -= 53
            rank = action % 13 + 1
            suit1 = self.double_combination[int(action/13)][0]
            suit2 = self.double_combination[int(action/13)][1]
            discard = [Card(rank, suit1), Card(rank, suit2)]
        elif action <= 182:
            # triple
            action -= 131
            rank = action % 13 + 1
            suit1 = self.triple_combination[int(action/13)][0]
            suit2 = self.triple_combination[int(action/13)][1]
            suit3 = self.triple_combination[int(action/13)][2]
            discard = [Card(rank, suit1), Card(rank, suit2), Card(rank, suit3)]
        elif action <= 195:
            action -= 183
            rank = action + 1
            # "Clubs", "Diamonds", "Hearts", "Spades"
            discard = [Card(rank, "Clubs"), Card(rank, "Diamonds"), Card(rank, "Hearts"), Card(rank, "Spades")]
        elif action <= 239:
            action -= 196
            suit = self.suits[int(action/11)]
            rank = action % 11 + 1
            discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit)]
        elif action <= 279:
            action -= 240
            suit = self.suits[int(action/10)]
            rank = action % 10 + 1
            discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit), Card(rank + 3, suit)]
        elif action <= 315:
            action -= 280
            suit = self.suits[int(action/9)]
            rank = action % 9 + 1
            discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit), Card(rank + 3, suit), Card(rank + 4, suit)]
        elif action <= 347:
            action -= 316
            suit = self.suits[int(action/8)]
            rank = action % 8 + 1
            discard = [Card(rank, suit), Card(rank + 1, suit), Card(rank + 2, suit), Card(rank + 3, suit), Card(rank + 4, suit), Card(rank + 5, suit)]
        return discard


if __name__ == '__main__':
    players = [RandomPlayer("Random1"), RandomPlayer("Random2")]

    game = GameEngine(players)
    # game.play_games(1)
    discard_cards = game.decode_action_discard(347)
    print(discard_cards)
