from rlcard import models
from yaniv_env import YanivEnv
from rlcard.agents.random_agent import RandomAgent

config = {}
env = YanivEnv(config)

random_agent = RandomAgent(action_num=env.action_num)
models.register('yaniv-dqn', 'pretrained_model:YanivDQNModel')
dqn_agent = models.load('yaniv-dqn').agents[0]
env.set_agents([dqn_agent, random_agent])

print(">> Yaniv pre-trained model")

while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)

    final_state = trajectories[0][-1][-2]

    #
    # print('===============     Result     ===============')
    # if payoffs[0] > 0:
    #     print('You win {} chips!'.format(payoffs[0]))
    # elif payoffs[0] == 0:
    #     print('It is a tie.')
    # else:
    #     print('You lose {} chips!'.format(-payoffs[0]))
    # print('')

    input("Press any key to continue...")