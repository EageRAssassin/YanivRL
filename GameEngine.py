from Cards import Card
from Deck import Deck
from numpy.random import shuffle
import math
import random
from BasePlayer import BasePlayer
from RandomPlayer import RandomPlayer
from ReinforcementLearning.utils import cards2str


class GameEngine:
    """Initializes a new game of Yaniv"""

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

        if player.decide_call_yaniv(self):
            game_over = True
            print(player, "calls Yaniv")
            return player, self.get_players_scores(player)

        ''' Discard phase '''
        discard_cards = player.decide_cards_to_discard(self)
        print("Player discards : ", [c for c in discard_cards])
        player.extract_cards(discard_cards)
        self.deck.discard(discard_cards)

        ''' Draw phase '''
        pile_to_draw_from, cards = player.decide_cards_to_draw(self)
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
        others_hands = self._get_others_current_hand(player)
        if self.is_over():
            actions = None
        else:
            actions = list(player.available_actions(self.round.greater_player, self.judger))
        state = {}
        state['deck'] = self.deck
        # seen cards
        # state['seen_cards'] = public['seen_cards']
        # state['trace'] = public['trace'].copy()
        state['self'] = self.player_id
        state['initial_hand'] = self.initial_hand
        state['current_hand'] = cards2str(self.players[player_id].show_cards())
        state['others_hand'] = others_hands
        state['actions'] = self.players[player_id].show_plays()
        # example of state
        # {
        #     'deck': '3333444455556666777788889999TTTTJJJJQQQQKKKKAAAA2222BR',
        #     'seen_cards': 'TQA',
        #     'self': 2,
        #     'initial_hand': '3456677799TJQKAAB',
        #     'trace': [(0, '8222'), (1, 'pass'), (2, 'pass'), (0, '6KKK'),
        #               (1, 'pass'), (2, 'pass'), (0, '8'), (1, 'Q')],
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


if __name__ == '__main__':
    players = [RandomPlayer("Random1"), RandomPlayer("Random2")]

    game = GameEngine(players)
    game.play_games(1)