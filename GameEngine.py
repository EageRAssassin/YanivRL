from Cards import Card
from Deck import Deck
from numpy.random import shuffle
import math
import random
from BasePlayer import BasePlayer
from RandomPlayer import RandomPlayer
from ReinforcementLearning.utils import decode_action_discard, encode_cards, encode_action_discard, cards_to_str


class GameEngine:
    """Initializes a new game of Yaniv"""

    def __init__(self, players):

        """init cards"""
        self.deck = Deck()
        self.players = players
        self.player_id = 0
        """init game vars"""
        self.game_over = False
        self.player_won = -1
        self.turn_number = 0
        self.state = {}

        """init player hands"""
        self.hands = [[self.deck.pop() for _ in range(7)] for player in players]

        for i in range(len(players)):
            players[i].add_cards_to_hand(self.hands[i])

        """init top of discard pile"""
        self.deck.previous_play = [self.deck.pop()]

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
        """ This function is for manual control of the game only """
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
                if pile_to_draw_from == "discard_pile":
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
                #     self.deck.append(prev_discard_cards)
                #     self.deck.remove(take_discard)
                # prev_discard_cards = discard_cards

    def step(self, action):
        """ Perform one step for the game for DQN """
        # select player
        player = self.players[self.player_id]

        # check action 0 -- player calls Yaniv
        if action == 0:
            game_over = True
            self.player_won = self.player_id
            self.player_id = (self.player_id + 1) % len(self.players)
            state = self.get_state(self.player_id)
            return player, state

        ''' Discard phase '''
        discard_cards = decode_action_discard(action)
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

    #TODO - fix this so that it also reads in the previous_play, since it
    #is NOT part of the discards pile
    def get_state(self, player_id):
        ''' Return player's state for DQN

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        player = self.players[player_id]
        state = {}
        state['deck'] = cards_to_str(self.deck.get_cards())
        state['discards'] = cards_to_str(self.deck.get_discards())
        state['self'] = self.player_id
        state['current_hand'] = cards_to_str(player.show_cards())
        # get the other player's hand
        others_hands = []
        for p_id in range(len(self.players)):
            if p_id != player_id:
                others_hands.append(cards_to_str(self.players[p_id].show_cards()))
        state['others_hand'] = others_hands
        state['actions'] = encode_action_discard(player.show_plays())
        return state

    def is_over(self):
        return self.game_over

    def get_payoff(self):
        # TODO may need more rules to ensure smaller cards get better awards
        # check if player won the game
        game_won_reward = 50 * (self.player_won == self.player_id)
        return -self.turn_number + game_won_reward


if __name__ == '__main__':
    players = [RandomPlayer("Random1"), RandomPlayer("Random2")]

    game = GameEngine(players)
    # game.play_games(1)
