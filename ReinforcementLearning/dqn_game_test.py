from rlcard import models
from rlcard.agents.random_agent import RandomAgent
from ReinforcementLearning.yaniv_env import YanivEnv

config = {}
env = YanivEnv(config)

random_agent = RandomAgent(action_num=env.action_num)
models.register('yaniv-dqn', 'pretrained_model:YanivDQNModel')
dqn_agent = models.load('yaniv-dqn').agents[0]
env.set_agents([dqn_agent, random_agent])

winner_list = []
game_round_number = 100

for game_round in range(game_round_number):

    trajectories, payoffs = env.run(is_training=False)
    # trajectories[0] means player 0
    # trajectories[0][-1] means player 0's last state
    # final_state = trajectories[0][-1]
    # print('player won is', env.game.player_won)
    winner_list.append(env.game.player_won)

print('DQN players won', winner_list.count(0), 'times in', game_round_number, 'game rounds')
print('Random players won', winner_list.count(1), 'times in', game_round_number, 'game rounds')
