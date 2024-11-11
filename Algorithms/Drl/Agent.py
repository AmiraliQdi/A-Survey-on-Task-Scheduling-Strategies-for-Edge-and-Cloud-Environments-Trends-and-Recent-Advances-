import copy
import random
from collections import deque

import numpy as np
import torch
from matplotlib import pyplot as plt


class Agent:

    def __init__(self, input_size, output_size, learning_rate=0.0009, target_network=False, epsilon=1, gamma=0.9,
                 mem_size=1000, mini_batch_size=64):
        self.nn = torch.nn.Sequential(
            torch.nn.Linear(input_size, 150),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(150, 150),
            torch.nn.LeakyReLU(),
            torch.nn.Linear(150, output_size),
            torch.nn.Softmax(dim=1),
        )

        # Second nn for stabilizing
        self.nn_stabilizer = copy.deepcopy(self.nn)
        self.target_network = target_network
        self.current_sync = 0

        # Hyper params
        self.epsilon = epsilon
        self.gamma = gamma

        # Attributes
        self.mem_size = mem_size
        self.batch_size = mini_batch_size
        self.mem = deque(maxlen=mem_size)
        self.action_size = output_size
        self.optimizer = torch.optim.Adam(self.nn.parameters(), lr=learning_rate)

        # Log
        self.loss_history = []

    def act(self, state):
        pred = self.nn(state)
        action = np.random.choice(self.action_size, p=pred.data.numpy().squeeze())
        return action, pred

    def experience_replay(self):
        if len(self.mem) >= self.batch_size:
            start = random.randint(0, len(self.mem) - self.batch_size)
            mini_batch = list(self.mem)[start:start + self.batch_size]
        else:
            return
        s1_batch = torch.cat([s1 for (s1, action, reward) in mini_batch])
        action_batch = torch.Tensor([action for (s1, action, reward) in mini_batch])
        reward_batch = torch.Tensor([reward for (s1, action, reward) in mini_batch])
        probs = self.nn(s1_batch)
        pred = probs.gather(dim=1, index=action_batch.long().view(-1, 1)).squeeze()
        # TODO use return and gamma
        loss = -1 * torch.sum(torch.log(pred + 1e-10) * reward_batch)
        return self.update(loss)

    def add_experience(self, experience):
        self.mem.append(experience)

    def update(self, loss):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.loss_history.append(loss.item())
        return loss.item()

    def save(self, path):
        torch.save({
            'model_state_dict': self.nn.state_dict(),
            'epsilon': self.epsilon,
            'gamma': self.gamma,
            'loss_history': self.loss_history
        }, path)

    def load(self, path):
        checkpoint = torch.load(path)
        self.nn.load_state_dict(checkpoint['model_state_dict'])
        self.epsilon = checkpoint['epsilon']
        self.gamma = checkpoint['gamma']
        self.loss_history = checkpoint['loss_history']

    def plot_loss(self):
        plt.bar(range(len(self.loss_history)), self.loss_history)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Loss History')
        plt.grid(True)
        plt.show()
