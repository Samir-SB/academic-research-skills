import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import argparse
import matplotlib.pyplot as plt
from collections import deque
import time
from sklearn.model_selection import train_test_split

from config_mgmt import load_config
from illinois_online import APSelectionEnv

torch.manual_seed(42)

# ----------------------------- 1. Neural Network -----------------------------
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim, dropout_prob = .5):
        super(QNetwork, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout_prob),
            nn.Linear(512, action_dim)
        )

    def forward(self, x):
        return self.fc(x)

# ----------------------------- 2. Replay Buffer -----------------------------
class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)

# ----------------------------- 3. Training Logic -----------------------------
def train_agent(env, num_episodes=50, batch_size=32, gamma=0.99, lr=5e-5):
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    
    q_net = QNetwork(state_dim, action_dim)
    target_net = QNetwork(state_dim, action_dim)
    target_net.load_state_dict(q_net.state_dict())
    
    optimizer = optim.Adam(q_net.parameters(), lr=lr)
    buffer = ReplayBuffer(20_000)
    
    epsilon = 1.0
    epsilon_decay = 0.95
    epsilon_min = 0.01
    
    rewards_history = []
    loss_history = deque(maxlen= 10_000) #[]

    for episode in range(num_episodes):
        state, _ = env.reset()
        episode_reward = 0
        done = False
        
        while not done:
            # Epsilon-greedy action selection
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    state_t = torch.FloatTensor(state.copy()).unsqueeze(0)
                    action = q_net(state_t).argmax().item()
            
            next_state, reward, terminated, truncated, _ = env.step(action)
            
            if reward == 0:
                if action == action_dim - 1:
                    reward = -.2
            
            done = terminated or truncated
            buffer.push(state, action, reward, next_state, done)
            state = next_state
            episode_reward += reward
            
            # Optimization Step
            if len(buffer) > batch_size:
                batch = buffer.sample(batch_size)
                s_batch, a_batch, r_batch, ns_batch, d_batch = zip(*batch)
                
                s_batch = torch.FloatTensor(np.array(s_batch))
                a_batch = torch.LongTensor(a_batch).unsqueeze(1)
                r_batch = torch.FloatTensor(r_batch).unsqueeze(1)
                ns_batch = torch.FloatTensor(np.array(ns_batch))
                d_batch = torch.FloatTensor(d_batch).unsqueeze(1)
                
                current_q = q_net(s_batch).gather(1, a_batch)
                max_next_q = target_net(ns_batch).max(1)[0].unsqueeze(1)
                target_q = r_batch + (gamma * max_next_q * (1 - d_batch))
                
                loss = nn.MSELoss()(current_q, target_q.detach())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                loss_history.append(loss.item())

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
        rewards_history.append(episode_reward)
        
        plot_results(rewards_history, loss_history)        
        print('Reward: ', episode_reward, 'epsilon: ', epsilon)
        
        # Update target network
        if episode % 5 == 0:
            target_net.load_state_dict(q_net.state_dict())
            torch.save(q_net.state_dict(), 'q_net.pth')
            print(f"Episode {episode+1}: Reward = {episode_reward:.2f}, Epsilon = {epsilon:.2f}")
            
        

    return rewards_history, loss_history

def plot_results(rewards, losses):
    plt.figure(figsize=(12, 5))

    # Plot Rewards
    plt.subplot(1, 2, 1)
    plt.plot(rewards, color='teal', label='Total Reward')
    plt.title('Reward per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Capacity')
    plt.grid(True, alpha=0.3)

    # Plot Loss
    plt.subplot(1, 2, 2)
    # Loss is plotted on a log scale often due to initial spikes
    plt.plot(losses, color='tomato', label='MSE Loss', alpha=0.6)
    plt.yscale('log')
    plt.title('Training Loss (Log Scale)')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('training.png')
    # plt.show()
    plt.close()

# ----------------------------- Main Processing -----------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train custom DQN from YAML config")
    parser.add_argument("--config", default="configs/exp1.yaml", help="Path to YAML config")
    args = parser.parse_args()
    config = load_config(args.config)

    # Load data
    data_path = config.data_dir / config.dataset.filename
    df = pd.read_csv(data_path)
    
    # split data into training and test data
    states_train, states_test = train_test_split(df, test_size=config.data_test_size, random_state=2)
    
    # logger.info(f"Test size: {TEST_SIZE} | Train: {len(states_train)} | Test: {len(states_test)}") 
    
    # Create environments
    final_nb_aps = config.env.final_nb_aps
    env = APSelectionEnv(
        states_train,
        num_aps=config.env.train.num_aps,
        on_line=config.env.train.on_line,
        final_nb_aps=final_nb_aps,
    )
    
    start_time = time.perf_counter()   
    
    rewards, losses = train_agent(env, num_episodes=50)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print('elapsed_time: ', elapsed_time)
    plot_results(rewards, losses)
