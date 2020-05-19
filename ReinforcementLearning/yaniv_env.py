import numpy as np

from BasePlayer import BasePlayer
from GameEngine import GameEngine
from Heuristic.HillClimbPlayer import HillClimbPlayer
from Heuristic.MinimaxPlayer import MinimaxPlayer
from Heuristic.SimulatedAnnealingPlayer import SimulatedAnnealingPlayer
from RandomPlayer import RandomPlayer
from ReinforcementLearning.env import Env
from ReinforcementLearning.utils import encode_cards


class YanivEnv(Env):
    """ Yaniv Environment
    """

    def __init__(self, config):
        super().__init__(config)

        # initialize the Yaniv game

        players = []

        # if player_config not specified in config, we initialize with two random player
        if not ('player_config' in config):
            players = [RandomPlayer("RandomPlayer1"), RandomPlayer("RandomPlayer2")]
        # otherwise we will find the player_config to generate players
        else:
            for i in range(len(config['player_config'])):
                player_type = config['player_config'][i]
                if player_type == 'DQN':
                    players.append(RandomPlayer('RDQNPlayer' + str(i)))
                elif player_type == 'Random':
                    players.append(RandomPlayer('RandomPlayer' + str(i)))
                elif player_type == 'HC':
                    players.append(HillClimbPlayer('HC' + str(i)))
                elif player_type == 'Minimax':
                    players.append(MinimaxPlayer('Minimax' + str(i)))
                elif player_type == 'SA':
                    players.append(SimulatedAnnealingPlayer('SA' + str(i)))

        self.game = GameEngine(players)
        self.state_shape = [4, 54]

    def init_game(self):
        """ Start a new game

        Returns:
            (tuple): Tuple containing:

                (numpy.array): The begining state of the game
                (int): The begining player
        """
        self.game.init_game()
        init_state = self.game.get_state(self.game.player_id)
        return self._extract_state(init_state), self.game.player_id

    def step(self, action, raw_action=False):
        """ Step forward

        Args:
            action (int): The action taken by the current player
            raw_action (boolean): True if the action is a raw action

        Returns:
            (tuple): Tuple containing:

                (dict): The next state
                (int): The ID of the next player
        """
        action = self._decode_action(action)
        self.timestep += 1
        next_state, player_id = self.game.step(action)
        return self._extract_state(next_state), player_id

    def _extract_state(self, state):
        """ Encode state

        Args:
            state (dict): dict of original state

        Returns:
            numpy array: 6*54 array
                         deck cards
                         discard cards
                         current hand
                         the union of the other two players' hand
        """
        obs = np.zeros((4, 54), dtype=int)
        obs[0] = encode_cards(state['deck'])
        obs[1] = encode_cards(state['discards'])
        obs[2] = encode_cards(state['current_hand'])
        obs[3] = encode_cards(state['others_hand'])

        extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions()}
        return extracted_state

    def get_player_id(self):
        """ Get the current player id

        Returns:
            (int): The id of the current player
        """
        self.get_player_id()

    def get_payoffs(self):
        """ Get the payoffs of players. Must be implemented in the child class.

        Returns:
            payoffs (list): a list of payoffs for each player
        """
        return self.game.get_payoff()

    def _decode_action(self, action_id):
        """ Action id -> the action in the game. Must be implemented in the child class.

        Args:
            action_id (int): the id of the action

        Returns:
            action (string): the action that will be passed to the game engine.
        """
        return action_id

    def _get_legal_actions(self):
        """ Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        """
        return self.game.state['actions']

    def _single_agent_step(self, action):
        """ Step forward for human/single agent

        Args:
            action (int): The action taken by the current player

        Returns:
            next_state (numpy.array): The next state
        """
        # self._single_agent_step(action)
        return
