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
    
    def getBid(self): 
        if np.random.rand() < self.epsilon:
            return random.randint(0, self.value - 1)
        else:
            return np.argmax(self.float_data[:, 1])  # Argmax over Q-values

    def updateAgent(self, i, training_episodes): 
        self.int_data[i, 2] += 1  # Increment the number of times bid i is used
        # Update win rate and Q-value
        if self.int_data[i, 2] > 0:  # Check to avoid division by zero
            self.float_data[i, 0] = self.int_data[i, 1] / self.int_data[i, 2]
            self.float_data[i, 1] = self.float_data[i, 0] * (self.value - i)
        
        decay_rate = 1-1/(0.5*training_episodes)
        
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
    def __init__(self, agents, gm, training_episodes): 
        self.agents = agents
        self.gameMode = gm

        #Getting the bids for each agent
        self.bids = []
        for x in agents: 
            bid = int(x.getBid())
            self.bids.append(bid)
            
        winner = self.getWinner(self.bids, self.gameMode)


        #UPDATE AGENTS
        for x in range(len(agents)): 
            ind = self.bids[x]
            agents[x].updateAgent(ind, training_episodes)
            if x == winner:
                agents[x].addWin(self.bids[winner]) 


    def getWinner(self, bids, gameMode): 
        maxIndex = np.argmax(bids)
        if gameMode == "standard": 
            return(maxIndex)
        elif gameMode == "second-price": 
            secondMax = float("-inf")
            secondMaxIndex = None
            for i, num in enumerate(bids):
                if num != max(bids) and num > secondMax:
                    secondMax = num
                    secondMaxIndex = i
            return(secondMaxIndex)    

def train(): 
    training_episodes = 100000
    values = "random" #Value generation either "random" (from 50 to 100) or "standard" (all 100)
    numAgents = 5
    gameMode = "second-price" # Gamemode either "second-price" or "standard"

    agents = []
    for x in range(numAgents): 
        v = makeValues(values)
        agents.append(agent(v))
    gameCount = 1
    for x in range(training_episodes): 
        g = game(agents, gameMode, training_episodes)
        gameCount += 1
        # Game has parameters for # of agents and gamemode 
   
    #Some summary testing data
    print(agents[1].value)
    print(np.sum(agents[1].int_data[:,1]))
    print(agents[1].int_data)
    print(agents[1].float_data)
        # NAV
        # We want to record data (as seen on the bottom of the doc, also come up with some more metrics we can take)
        #you don't have to do this here ofc, but after we get the game running we need to figure it out
        
    
def makeValues(values): 
    if values == "standard": 
        return(100)
    else: 
        v = random.randint(50, 100) # We can edit these parameters 
        #we shld try and incorporate PyTorch seed values so this can be recreated
        #fairly low priority tho, this is prob the last thing we'd do 
        return(v)

train()
#Edit the train method


# Current priority list: 
# Making a way to deal with two people bidding the same value 
# Gathering advanced data
# Reproducible PyTorch seed values 