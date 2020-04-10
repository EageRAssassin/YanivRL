import numpy as np

from GameEngine import GameEngine
from RandomPlayer import RandomPlayer
from ReinforcementLearning.env import Env
from ReinforcementLearning.utils import ACTION_LIST


class YanivEnv(Env):
    """ Yaniv Environment
    """

    def __init__(self, config):
        super().__init__(config)

        # initialize the yaniv game

        players = [RandomPlayer("Random1"), RandomPlayer("Random2")]
        self.game = GameEngine(players)

        # TODO to be discussed and changed
        self.state_shape = [6, 5, 15]

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
        self.step(action, raw_action)

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
            numpy array: 6*5*15 array
                         6 : current hand
                             the union of the other two players' hand
                             the recent three actions
                             the union of all played cards
        """
        obs = np.zeros((6, 5, 15), dtype=int)
        for index in range(6):
            obs[index][0] = np.ones(15, dtype=int)
        encode_cards(obs[0], state['current_hand'])
        encode_cards(obs[1], state['others_hand'])
        for i, action in enumerate(state['trace'][-3:]):
            if action[1] != 'pass':
                encode_cards(obs[4-i], action[1])
        if state['played_cards'] is not None:
            encode_cards(obs[5], state['played_cards'])

        extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions()}
        if self.record_action:
            extracted_state['action_record'] = self.action_recorder
        return extracted_state

    def get_player_id(self):
        """ Get the current player id

        Returns:
            (int): The id of the current player
        """
        self.get_player_id()

    def get_state(self, player_id):
        """ Get the state given player id

        Args:
            player_id (int): The player id

        Returns:
            (numpy.array): The observed state of the player
        """
        # TODO
        self.get_state(player_id)

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
        abstract_action = ACTION_LIST[action_id]
        # without kicker
        if '*' not in abstract_action:
            return abstract_action
        # with kicker
        legal_actions = self.game.state['actions']
        specific_actions = []
        kickers = []
        for legal_action in legal_actions:
            for abstract in SPECIFIC_MAP[legal_action]:
                main = abstract.strip('*')
                if abstract == abstract_action:
                    specific_actions.append(legal_action)
                    kickers.append(legal_action.replace(main, '', 1))
                    break
        # choose kicker with minimum score
        player_id = self.game.get_player_id()
        kicker_scores = []
        for kicker in kickers:
            score = 0
            for action in self.game.judger.playable_cards[player_id]:
                if kicker in action:
                    score += 1
            kicker_scores.append(score+CARD_RANK_STR.index(kicker[0]))
        min_index = 0
        min_score = kicker_scores[0]
        for index, score in enumerate(kicker_scores):
            if score < min_score:
                min_score = score
                min_index = index
        return specific_actions[min_index]

    def _get_legal_actions(self):
        """ Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        """
        # TODO
        legal_action_id = []
        legal_actions = self.game.state['actions']
        # if legal_actions:
        #     for action in legal_actions:
        #         for abstract in SPECIFIC_MAP[action]:
        #             action_id = ACTION_SPACE[abstract]
        #             if action_id not in legal_action_id:
        #                 legal_action_id.append(action_id)
        legal_action_id = []

        return legal_action_id

    def _single_agent_step(self, action):
        """ Step forward for human/single agent

        Args:
            action (int): The action taken by the current player

        Returns:
            next_state (numpy.array): The next state
        """
        self._single_agent_step(action)
