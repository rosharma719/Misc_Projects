import numpy as np
from matplotlib import pyplot as plt 
import random
import math

class agent: 
    def __init__(self, value): 
        self.value = value
        self.epsilon = 1
        # Integer data: Bid value, #wins, #games bidded with this value
        self.int_data = np.zeros((value, 3), dtype=int)
        for x in range(value): 
            self.int_data[x, 0] = x
        # Floating-point data: Win rate, Q-value
        self.float_data = np.ones((value, 2))  # Initialized with ones to avoid division by zero
        for x in range(value): 
            self.float_data[x, 1] = 1+math.floor(5 * random.random())
    
    def getBid(self, agents): 
        if np.random.rand() < self.epsilon:
            return random.randint(0, self.value - 1)
        else:
            predictedArr = []
            for x in agents: 
                if x != self: 
                    predictedArr.append(np.argmax(self.float_data[:,1]))
            return(max(predictedArr) +1)
            #return np.argmax(self.float_data[:, 1])  # Argmax over Q-values

    def updateAgent(self, i, training_episodes, episode): 
        self.int_data[i, 2] += 1  # Increment the number of times bid i is used
        # Update win rate and Q-value
        if self.int_data[i, 2] > 0:  # Check to avoid division by zero
            self.float_data[i, 0] = self.int_data[i, 1] / self.int_data[i, 2]
            self.float_data[i, 1] = self.float_data[i, 0] * (self.value - i)
        
        decay_rate = 1-1/(0.3*training_episodes)
        
        if decay_rate > 0: 
            self.epsilon = self.epsilon*decay_rate


    def addWin(self, i): 
        self.int_data[i, 1] += 1  # Increment the number of wins for bid i
        # Update win rate and Q-value
        if self.int_data[i, 2] > 0: 
            self.float_data[i, 0] = self.int_data[i, 1] / self.int_data[i, 2]
            self.float_data[i, 1] = self.float_data[i, 0] * (self.value - i) 
            # Multiples of self.value (value) or i (bid payment) will affect their weighting and equilibrium 


class game: 
    def __init__(self, agents, gm, training_episodes, episode): 
        self.agents = agents
        self.gameMode = gm

        #Getting the bids for each agent
        self.bids = []
        for x in agents: 
            bid = int(x.getBid(agents))
            self.bids.append(bid)
            
        winner = self.getWinner(self.bids, self.gameMode)
        self.winning_value = self.bids[winner]

        #UPDATE AGENTS
        for x in range(len(agents)): 
            ind = self.bids[x]
            agents[x].updateAgent(ind, training_episodes, episode)
            if x == winner:
                agents[x].addWin(self.bids[winner]) 
        

    def getWinner(self, bids, gameMode): 
        if gameMode == "standard": 
            max_bid = max(bids)
            num_max_bids = bids.count(max_bid)
            if num_max_bids > 1:
                tied_agents = [i for i, x in enumerate(bids) if x == max_bid]
                random.shuffle(tied_agents)
                return random.choice(tied_agents)
            else:
                    return bids.index(max_bid)
        elif gameMode == "second-price":
            # Sort bids and find the second unique maximum value
            unique_sorted_bids = sorted(set(bids), reverse=True)
            if len(unique_sorted_bids) >= 2:
                secondMax = unique_sorted_bids[1]
                secondMaxIndices = [i for i, x in enumerate(bids) if x == secondMax]
                return random.choice(secondMaxIndices)  # Randomly choose if there are multiple second max
            else:
                # If there is no second max (all bids are equal), pick a random winner
                return random.randint(0, len(bids) - 1)


def train(): 
    training_episodes = 10000
    values = "standard" #Value generation either "random" (from 50 to 100) or "standard" (all 100)
    numAgents = 3
    gameMode = "standard" # Gamemode either "second-price" (second-highest price) or "standard"

    agents = []
    for x in range(numAgents): 
        v = makeValues(values)
        agents.append(agent(v))
    gameCount = 1

    #Prep for some summary stats
    bidArr = np.empty((0, len(agents)), int)
    winArr = []


    
    win_rates = []  # Stores win rates of agents for analysis
    avg_bids = []   # Stores average bids of agents for analysis
    #Running the game
    for episode in range(training_episodes): 
        #Create a new game, with parameters for # of agents and gamemode 
        g = game(agents, gameMode, training_episodes, episode)

        bidArr = np.vstack((bidArr, g.bids))
        winArr.append(g.winning_value)
        gameCount += 1

        agent_wins = [agent.int_data[:, 1].sum() for agent in agents]
        agent_bids = [np.argmax(agent.float_data[:, 1]) for agent in agents]

        win_rates.append(agent_wins)
        avg_bids.append(agent_bids)
   
    #More summary debug and stat info
    print(agents[1].value)
    print(np.sum(agents[1].int_data[:,1]))
    winPlot(winArr)
    
    getWinRates(win_rates, avg_bids, training_episodes, agents)

    # Visualization and analysis

def getWinRates(win_rates, avg_bids, training_episodes, agents):
    win_rates = np.array(win_rates)
    avg_bids = np.array(avg_bids)

    # Plots win rates of each agent over episodes
    for i, agent_wins in enumerate(win_rates.T):
        plt.plot(range(training_episodes), agent_wins, marker = '.', linestyle = '', label=f"Agent {i}")

    plt.xlabel('Episodes')
    plt.ylabel('Total Wins')
    plt.title('Total Wins Per Agent')
    plt.legend()
    plt.show()

    # Plots average bids of each agent over episodes
    for i, agent_bids in enumerate(avg_bids.T):
        plt.plot(range(training_episodes), agent_bids, marker = '.', linestyle = '', label=f"Agent {i}")

    plt.xlabel('Episodes')
    plt.ylabel('Bid Value')
    plt.title('Average Bid Value Per Game')
    plt.legend()
    plt.show()

    # Displays agent's value and games won by agents
    for idx, ag in enumerate(agents):
        print(f"Agent {idx} value:", ag.value)
        print(f"Games won by Agent {idx}:", ag.int_data[:, 1].sum(), "of", training_episodes)

def winPlot(list_1d):
    # The length of x_values should match the number of games played
    num_games = len(list_1d)
    x_values = range(1, num_games + 1)

    # Plot the list of winning bids
    plt.plot(x_values, list_1d, marker='.', linestyle = '', color='blue', label='Winning Bid')

    # Adding labels and title
    plt.xlabel('Game Number')
    plt.ylabel('Bid Value')
    plt.title('Winning Bids Over Time')
    plt.legend()

    # Show the plot
    plt.show()

    # Call the plotting function with actual data from the training


def makeValues(values): 
    if values == "standard": 
        return(100)
    else: 
        v = random.randint(50, 100) 
        return(v)  

train()
#Edit the train method

