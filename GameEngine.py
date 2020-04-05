from Cards import Card
from Deck import Deck
from numpy.random import shuffle
import math
import random
from BasePlayer import BasePlayer
from RandomPlayer import RandomPlayer

class GameEngine:
    """Initializes a new game of Yaniv"""

    def __init__(self, players):

        """init cards"""
        self.deck = Deck()
        self.players = players

        """init game vars"""
        # self.game_over = False
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

    def get_players_scores(self, yaniv_caller):
        scores_dict = {}
        for player in self.players:
            if player is yaniv_caller:
                    scores_dict[player.id] = 0
            else:
                scores_dict[player.id] = player.get_hand_value()
        return scores_dict


if __name__ == '__main__':
    players = [RandomPlayer("Random1"), RandomPlayer("Random2")]

    game = GameEngine(players)
    game.play_games(1)