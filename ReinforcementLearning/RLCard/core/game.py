import rlcard


class YanivGame(rlcard.core.Game):
    ''' Game class. This class will interact with outer environment.
    '''

    def init_game(self):
        ''' Initialize all characters in the game and start round 1
        '''
        raise NotImplementedError

    def step(self, action):
        ''' Perform one draw of the game and return next player number, and the state for next player
        '''
        raise NotImplementedError

    def step_back(self):
        ''' Takes one step backward and restore to the last state
        '''
        raise NotImplementedError

    def get_player_num(self):
        ''' Retrun the number of players in the game
        '''
        raise NotImplementedError

    def get_action_num(self):
        ''' Return the number of possible actions in the game
        '''
        raise NotImplementedError

    def get_player_id(self):
        ''' Return the current player that will take actions soon
        '''
        raise NotImplementedError

    def is_over(self):
        ''' Return whether the current game is over
        '''
        raise NotImplementedError