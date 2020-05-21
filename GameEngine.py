from Deck import Deck
from numpy.random import shuffle
import math
import random
from BasePlayer import BasePlayer
from RandomPlayer import RandomPlayer
from ReinforcementLearning.utils import decode_action_discard, encode_cards, encode_action_discard, cards_to_str


class GameEngine:
    """Initializes a new game of Yaniv"""

    def __init__(self, players_input):
        self.player_id = 0
        self.players = players_input
        self.game_over = False
        self.player_won = -1
        self.turn_number = 0
        self.deck = Deck()
        self.state = {}
        self.history = []
        #format for hand_history:
        #[[first player's public hand], [second player's public hand]...]
        self.hand_history = []

    def init_game(self):
        """reinitialize the attributes"""
        self.player_id = 0
        # clear the current hand of the players
        self.hand_history = [[None for _ in range(7)] for _ in range(len(self.players))]
        for i in range(len(self.players)):
            self.players[i].hand = []
        self.game_over = False
        self.player_won = -1
        self.turn_number = 0
        self.deck = Deck()
        """init cards"""
        self.deal_card()
        self.state = self.get_state(0)
        """init top of discard pile"""
        self.deck.previous_play = [self.deck.cards.pop()]

    def get_num_players(self):
        return len(self.players)

    def get_top_discards(self):
        return self.deck.get_top_discards()

    def get_top_card(self):
        return self.deck.get_top_card()

    def play_games(self, num_games, verbose=True, shuffle=False):
        running_scores = {}
        total_wins = {}
        for player in self.players:
            running_scores[player.id] = 0
            total_wins[player.id] = 0

        for i in range(num_games):
            if (shuffle):
                random.shuffle(self.players)
            if (i % 50 == 0):
                print("Game " + str(i))
            self.init_game()
            winning_player, current_round_scores = self.game_loop(verbose)
            for player in self.players:
                running_scores[player.id] += current_round_scores[player.id]
                if current_round_scores[player.id] == 0:
                    total_wins[player.id] += 1

        return running_scores, total_wins

    def deal_card(self):
        for player in self.players:
            cards = [self.deck.draw_top_card() for _ in range(7)]
            player.add_cards_to_hand(cards)

    def game_loop(self, verbose=True, max_round=1000):
        """ This function is for manual control of the game only """
        round_cnt = 0

        while round_cnt < max_round:
            if (verbose): print("======== Round " + str(round_cnt) + " =========")
            for player in self.players:
                if (verbose): print("----- Current player :" + str(player) + "-------")
                player_hand = player.show_cards()
                if (verbose): print("Player's hand: ", [c for c in player_hand])
                # if player.decide_call_yaniv(self):
                #     print(player, "calls Yaniv")
                #     return player, self.get_players_scores(player)
                ''' Discard phase '''
                discard_cards = player.decide_cards_to_discard(self)

                if not discard_cards:
                    if (verbose): print(player, "calls Yaniv")
                    return player, self.get_players_scores(player)

                if (verbose): print("Player discards : ", [c for c in discard_cards])
                player.extract_cards(discard_cards)
                self.deck.discard(discard_cards)

                ''' Draw phase '''
                pile_to_draw_from, card = player.decide_cards_to_draw(self)
                if pile_to_draw_from == "discard_pile":
                    discard_top = self.deck.draw_top_discard(card)
                    player.add_cards_to_hand([discard_top])
                elif pile_to_draw_from == "unseen_pile":
                    card = self.deck.draw_top_card()
                    player.add_cards_to_hand([card])
                if (verbose): print("Player draws from : ", pile_to_draw_from)

                ''' Tracking the play that was just made '''
                ''' Format: player ID, the card(s) discarded, the pile drawn from, and the card taken (None if taken from deck) '''
                history_tuple = (player.id, discard_cards, pile_to_draw_from, card)
                self.history.append(history_tuple)


                ''' Updating hand_history '''
                current_public_hand = self.hand_history[self.player_id]
                for discarded_card in discard_cards:
                    if discarded_card in current_public_hand:
                        current_public_hand.remove(discarded_card)
                    else:
                        current_public_hand.remove(None)
                if pile_to_draw_from == "discard_pile":
                    current_public_hand.append(card)
                else:
                    current_public_hand.append(None)
                self.hand_history[self.player_id] = current_public_hand


                round_cnt += 1
                self.player_id = (self.player_id + 1) % len(self.players)
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
        # print("----- Current player :" + str(self.player_id) + "------- with action " + str(action))
        player_hand = player.show_cards()
        # print("Player's hand: ", [c for c in player_hand])

        ''' Discard phase '''
        # if that is a Hill Climbing player, it will decide its own actions
        if 'HC' in player.id:
            discard_cards = player.decide_cards_to_discard(self)

            if not discard_cards:
                self.game_over = True
                self.player_won = self.player_id
                self.player_id = (self.player_id + 1) % len(self.players)
                state = self.get_state(self.player_id)
                return state, self.player_id

            player.extract_cards(discard_cards)
            self.deck.discard(discard_cards)
        # game engine will use the action id from environment to perform else
        else:
            # check action 0 -- player calls Yaniv
            if action == 0:
                self.game_over = True
                self.player_won = self.player_id
                self.player_id = (self.player_id + 1) % len(self.players)
                state = self.get_state(self.player_id)
                return state, self.player_id

            discard_cards = decode_action_discard(action)
            player.extract_cards(discard_cards)
            self.deck.discard(discard_cards)
            # print("Player discards : ", [c for c in discard_cards])

        ''' Draw phase '''
        pile_to_draw_from, card = player.decide_cards_to_draw(self)
        if pile_to_draw_from == "discard_pile":
            discard_top = self.deck.draw_top_discard(card)
            player.add_cards_to_hand([discard_top])
        elif pile_to_draw_from == "unseen_pile":
            card = self.deck.draw_top_card()
            player.add_cards_to_hand([card])

        # print("Player draws from : ", pile_to_draw_from)
        self.turn_number += 1
        self.player_id = (self.player_id + 1) % len(self.players)
        # get next state
        self.state = self.get_state(self.player_id)
        return self.state, self.player_id

    def get_players_scores(self, yaniv_caller):
        scores_dict = {}
        for player in self.players:
            if player is yaniv_caller:
                scores_dict[player.id] = 0
            else:
                scores_dict[player.id] = player.get_hand_value()
        return scores_dict

    # TODO - fix this so that it also reads in the previous_play, since it
    # is NOT part of the discards pile
    def get_state(self, player_id):
        """ Return player's state for DQN

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        """
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
                others_hands.extend(cards_to_str(self.players[p_id].show_cards()))
        state['others_hand'] = others_hands
        state['actions'] = encode_action_discard(player.show_plays())
        return state

    def get_other_player_hands(self, player_id):
        return self.hand_history[player_id + 1 : len(self.players)] + self.hand_history[0 : player_id]

    def is_over(self):
        return self.game_over

    def get_payoff(self):
        # check if player won the game
        payoff = [0 for i in range(len(self.players))]
        for i in range(len(self.players)):
            if i != self.player_won:
                payoff[self.player_id] = -self.players[i].get_hand_value()
            # compensate for the turn number, shorter is better
            payoff[self.player_id] -= 1 + self.turn_number
        return payoff


if __name__ == '__main__':
    players = [RandomPlayer("Random1"), RandomPlayer("Random2")]
    game = GameEngine(players)
    game.play_games(1)
