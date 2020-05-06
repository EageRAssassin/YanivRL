from rlcard.models.model import Model
from yaniv_env import YanivEnv
from rlcard.agents.dqn_agent import DQNAgent

class YanivDQNModel(Model):

    def __init__(self):
        ''' Load pretrained model
        '''
        import tensorflow as tf

        self.graph = tf.Graph()
        self.sess = tf.Session(graph=self.graph)

        env = YanivEnv({})
        with self.graph.as_default():
            self.dqn_agents = []
            agent = DQNAgent(self.sess,
                             scope='dqn',
                             action_num=env.action_num,
                             replay_memory_init_size=1000,
                             train_every=1,
                             state_shape=env.state_shape,
                             mlp_layers=[512, 512]
                             )
            self.dqn_agents.append(agent)

        with self.sess.as_default():
            with self.graph.as_default():
                saver = tf.train.Saver()
                saver.restore(self.sess, tf.train.latest_checkpoint('models/yaniv_dqn'))

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game
        Returns:
            agents (list): A list of agents
        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.dqn_agents