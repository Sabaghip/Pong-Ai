import pong
import random

class Counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def argMax(self):
        if len(list(self.keys())) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]




class agent:
    def __init__(self, alpha, numberOfTrain,discount=1):
        self.discount = discount
        self.alpha = alpha
        self.qValues = Counter()
        self.pong = pong.Pitch(18, 7, 5, 12)
        for i in range(numberOfTrain):
            state = self.pong.getState()
            action = self.getAction(state)
            reward = self.pong.play(0, action=action, train=True)
            self.update(state, action, self.pong.getState(), reward)
        while True:
            self.pong.play(0.1, action=self.computeActionFromQValues(self.pong.getState()))
    
    def update(self, state, action, nextState, reward):
        bestAction = self.computeActionFromQValues(nextState)
        sample = reward + self.discount * self.qValues[(nextState, bestAction)]
        self.qValues[(state, action)] = (1 - self.alpha) * self.qValues[(state, action)] + self.alpha * sample
        return

    def computeActionFromQValues(self, state):
        legalActions = self.getLegalActions(state)
        action = None
        max = -100000
        for action1 in legalActions:
          if self.qValues[(state, action1)] > max:
            max = self.qValues[(state, action1)]
            action = action1
        return action
    
    def getLegalActions(self, state):
        if state[1] == 1:
            return(0,2)
        if state[1] == 5:
            return(0,1)
        return (0, 1, 2)

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
          return None
        action = random.choice(legalActions)
        return action

if __name__=="__main__":
    agent = agent(alpha=0.5, numberOfTrain=1000000)
