from rlcard import models
from rlcard.agents.random_agent import RandomAgent

from Heuristic.HillClimbPlayer import HillClimbPlayer
from ReinforcementLearning.yaniv_env import YanivEnv

config = {'player_config': ['DQN', 'Random', 'HC']}
env = YanivEnv(config)

random_agent = RandomAgent(action_num=env.action_num)
models.register('yaniv-dqn', 'pretrained_model:YanivDQNModel')
dqn_agent = models.load('yaniv-dqn').agents[0]
# We have three agents in this environment, and the second and third ones are trivial
# the players will step by itself in the game engine
env.set_agents([dqn_agent, random_agent, random_agent])

winner_list = []
score_list = []
game_round_number = 100

for game_round in range(game_round_number):
    trajectories, payoffs = env.run(is_training=False)
    winner_list.append(env.game.player_won)
    score_list.append(env.game.get_players_scores(env.game.player_won))

print('DQN player won', winner_list.count(0), 'times in', game_round_number, 'game rounds')
print('Random player won', winner_list.count(1), 'times in', game_round_number, 'game rounds')
print('Hill Climb player won', winner_list.count(2), 'times in', game_round_number, 'game rounds')
print('The score list for the games is', score_list)
