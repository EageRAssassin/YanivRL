import numpy as np

from BasePlayer import BasePlayer
from GameEngine import GameEngine
from RandomPlayer import RandomPlayer
from ReinforcementLearning.env import Env
from ReinforcementLearning.utils import encode_cards


class YanivEnv(Env):
    """ Yaniv Environment
    """

    def __init__(self, config):
        super().__init__(config)

        # initialize the Yaniv game
        players = [BasePlayer("BasePlayer1"), BasePlayer("BasePlayer2"), BasePlayer("BasePlayer3")]
        self.game = GameEngine(players)
        self.state_shape = [4, 54]

    def init_game(self):
        """ Start a new game

        Returns:
            (tuple): Tuple containing:

                (numpy.array): The begining state of the game
                (int): The begining player
        """
        self.init_game()

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

    def set_agents(self, agents):
        """ Set the agents that will interact with the environment

        Args:
            agents (list): List of Agent classes
        """
        self.set_agents(agents)

    def run(self, is_training=False, seed=None):
        """ Run a complete game, either for evaluation or training RL agent.

        Args:
            is_training (boolean): True if for training purpose.
            seed (int): A seed for running the game. For single-process program,
              the seed should be set to None. For multi-process program, the
              seed should be assigned for reproducibility.

        Returns:
            (tuple) Tuple containing:

                (list): A list of trajectories generated from the environment.
                (list): A list payoffs. Each entry corresponds to one player.

        Note: The trajectories are 3-dimension list. The first dimension is for different players.
              The second dimension is for different transitions. The third dimension is for the contents of each transiton
        """
        self.run(is_training, seed)

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
        obs[3] = encode_cards(state['played_cards'])

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
        self._single_agent_step(action)
