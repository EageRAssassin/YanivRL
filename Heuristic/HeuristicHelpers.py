import numpy as np

HILL_CLIMB_PENALTY_PER_TURN = 15
HILL_CLIMB_RANDOM_CARD_VALUE = 8

SIMULATED_ANNEALING_PENALTY_PER_TURN = 15

def argsmax(list):
    return np.argwhere(list == np.amax(list)).flatten().tolist()
