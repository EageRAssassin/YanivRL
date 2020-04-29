import numpy as np


#Hill Climbing Algorithm Variables
HILL_CLIMB_PENALTY_PER_TURN = 15

#If FIXED_RANDOM_VALUE is True, then assume drawing a random card costs RANDOM_CARD_FIXED_VALUE
HILL_CLIMB_FIXED_RANDOM_VALUE = False
HILL_CLIMB_RANDOM_CARD_FIXED_VALUE = 7
#Else assume random card value decreases as game progresses
HILL_CLIMB_RANDOM_CARD_INIT_VALUE = 10

SIMULATED_ANNEALING_PENALTY_PER_TURN = 15
SIMULATED_ANNEALING_RANDOM_CARD_VALUE = 8

def argsmax(list):
    return np.argwhere(list == np.amax(list)).flatten().tolist()
