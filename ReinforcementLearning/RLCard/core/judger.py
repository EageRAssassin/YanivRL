import rlcard


class YanivJudger(rlcard.core.Judger):
    """ Judger decides whether the round/game ends and return the winner of the round/game
    """

    def judge_game(self, **kwargs):
        """ Decide whether the game ends, and return the winner of the game
        Returns:
            int: return the player's id who wins the game or -1 meaning the game has not ended
        """
        # need to think about a way to track the player who calls Yaniv
        raise NotImplementedError
