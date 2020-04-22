import numpy as np

HILL_CLIMB_PENALTY_PER_TURN = 15

SIMULATED_ANNEALING_PENALTY_PER_TURN = 15

def argsmax(list):
    return np.argwhere(list == np.amax(list)).flatten().tolist()
