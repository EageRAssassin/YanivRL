import numpy as np

def argsmax(list):
    return np.argwhere(list == np.amax(list)).flatten().tolist()

"""#region Hill Climb"""
HILL_CLIMB_PENALTY_PER_TURN = 15 #prioritise multi card throw over singles

#If FIXED_RANDOM_VALUE is True, then assume drawing a random card costs RANDOM_CARD_FIXED_VALUE
HILL_CLIMB_FIXED_RANDOM_VALUE = False
HILL_CLIMB_RANDOM_CARD_FIXED_VALUE = 7 #prioritise taking from random pile instead of discarded pile
#Else assume random card value decreases as game progresses
HILL_CLIMB_RANDOM_CARD_INIT_VALUE = 10 #prioritise taking from random pile instead of discarded pile


"""#region Simulated Annealing"""
SIMULATED_ANNEALING_PENALTY_PER_TURN = 15

#If FIXED_RANDOM_VALUE is True, then assume drawing a random card costs RANDOM_CARD_FIXED_VALUE
SIMULATED_ANNEALING_FIXED_RANDOM_VALUE = False
SIMULATED_ANNEALING_RANDOM_CARD_FIXED_VALUE = 7
#Else assume random card value decreases as game progresses
SIMULATED_ANNEALING_RANDOM_CARD_INIT_VALUE = 10

#If LINEAR_COOLING, then start at INITIAL_TEMPERATURE and cool by FIXED_COOLING_VALUE every turn
SIMULATED_ANNEALING_LINEAR_COOLING = False
SIMULATED_ANNEALING_FIXED_INITIAL_TEMPERATURE = 15
SIMULATED_ANNEALING_FIXED_COOLING_VALUE = 1

"""#region Minimax"""
MINIMAX_DEPTH = 3

MINIMAX_PENALTY_PER_TURN = 15
#If FIXED_RANDOM_VALUE is True, then assume drawing a random card costs RANDOM_CARD_FIXED_VALUE
MINIMAX_FIXED_RANDOM_VALUE = False
MINIMAX_RANDOM_CARD_FIXED_VALUE = 7
#Else assume random card value decreases as game progresses
MINIMAX_RANDOM_CARD_INIT_VALUE = 10
