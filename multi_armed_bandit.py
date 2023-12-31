# -*- coding: utf-8 -*-
"""
Authors:

Jairo El Yazidi Ríos
Tea Shkurti

# 
In this task we will simulate the example of multi-armed bandit presented in the lecture. Note that, differently from the previous topics, Reinforcement Learning is a online method. Therefore we cannot rely on offline datasets. We will, then use simulations.
"""

import numpy as np
import matplotlib.pyplot as plt

class MAB:
    def __init__(self, K):
        self.q_star = np.random.normal(0, 1, K)
    def play(self,a):
        return np.random.normal(self.q_star[a], 1, 1)[0]
    def getK(self):
        return self.q_star.shape[0]
    
np.random.seed(50)

"""Here we consider that we have a slot machine with $K=10$ arms. Each arm have a mean expeted reward sampled from a normal distribution with zero mean and variance 1. A toy example with just two simulations for each arm """

def simulate(mab,nsim):
    sim = np.zeros(mab.getK()*nsim).reshape(mab.getK(),nsim)
    for i in range(nsim):
        for a in range(mab.getK()):
            sim[a,i] = mab.play(a)
    return sim

def boxplot(data):
    fig = plt.figure(figsize =(5,3))
    ax = fig.add_axes([0, 0, 1, 1])
    bp = ax.boxplot(data, showfliers=False)
    plt.show()

K=10
nsim = 2
mab = MAB(10)

data = simulate(mab,3)
boxplot(data.T)

"""Lets increase the number of simulations in order to (explore) have more confidence regarding the mean of each arm:"""

data = simulate(mab,10)
boxplot(data.T)

data = simulate(mab,50)
boxplot(data.T)

data = simulate(mab,10000)
boxplot(data.T)

data = simulate(mab,100000)
boxplot(data.T)

"""

```
# This is formatted as code
```

Cummulative reward in the exploration step:"""

nSim = 100
data = simulate(mab,nSim)
print(np.sum(data))

"""What would happen if we new in advance the best arm:"""

bestArm = 5#check the best arm
reward = 0
for i in range(nSim*K):
    reward = reward + mab.play(bestArm-1)

reward

"""Lets assume exploration time of $10$ units for each arm """

T = 1000
explorationInterval = 10
explorationArm =  simulate(mab,explorationInterval) 
bestArm = np.argmax(explorationArm.mean(axis = 1))

rewardExploration = explorationArm.reshape(explorationArm.shape[0]*explorationArm.shape[1],)
print(f"EXPLORATION: # of plays: {rewardExploration.shape[0]} | Reward: {rewardExploration.sum()} ({rewardExploration.mean()})")

rewardExploitation = np.zeros(T - explorationInterval * mab.getK())
for i in range(rewardExploitation.shape[0]):
    rewardExploitation[i] = mab.play(bestArm)

print(f"EXPLOITATION: arm: {bestArm + 1} | # of plays: {rewardExploitation.shape[0]} | Reward: {rewardExploitation.sum()} ({rewardExploitation.mean()})")


finalReward = np.r_[rewardExploration,rewardExploitation]
print(f"FINAL # of plays: {finalReward.shape[0]} | Reward: {finalReward.sum()} ({finalReward.mean()})")

"""We are working with stochastic processes here. So just one simulation is not enough to take conclusions. We will here try different exploration/exploitation regimes to undersdant the exploration exploitation dilemna."""

def run(mab,T,selectInterval):
    selectArm =  simulate(mab,selectInterval) 
    bestArm = np.argmax(selectArm.mean(axis = 1))
    rewardSelect = selectArm.reshape(selectArm.shape[0]*selectArm.shape[1],)
    rewardBest = np.zeros(T - selectInterval * mab.getK())
    for i in range(rewardBest.shape[0]):
        rewardBest[i] = mab.play(bestArm)
    finalReward = np.r_[rewardSelect,rewardBest]
    return rewardSelect,rewardBest,finalReward

T=1000
nSim = 5000
rangeSelect = 20 + 1
simMatrix = np.zeros(rangeSelect*nSim).reshape(rangeSelect,nSim)

for rs in range(1,rangeSelect):
    print(f"Simulating for {rs}")
    for s in range(nSim):
        _,_,finalReward = run(mab,T,rs)
        simMatrix[rs,s] = np.sum(finalReward)

"""Plotting the results"""

plt.xticks(np.arange(1,rangeSelect), np.arange(1,rangeSelect))
plt.plot(np.arange(1,rangeSelect), simMatrix.mean(axis=1)[range(1,rangeSelect)]);

"""## Task 

In this task we will test the $\epsilon$-greed algorithm for MAB.For that, lets simulate the algorithm for different values of $\epsilon$ by keeping the simulation procedure used in this tutorial. Compare the results with the ones obtained above
"""

import random

def run_sim(mab, T, e):
  Q = np.zeros(mab.getK())
  N = np.zeros(mab.getK())
  reward = 0
  for i in range(0, T):
    rand = random.random()
    if rand > e:
      chosen = np.argmax(Q)
    else:
      chosen = int(random.random() * mab.getK())
    rew = mab.play(chosen)
    N[chosen] = N[chosen] + 1
    Q[chosen] = Q[chosen] + 1 / N[chosen] * (rew - Q[chosen])
    reward = reward + rew
  return reward

T=1000
nSim = 5000
rangeEpsilon = [0,0.001,0.005,0.1,0.5]
mab = MAB(10)
rew = []
for e in rangeEpsilon:
  reward = 0
  for n in range(0, nSim):
    reward = reward + run_sim(mab, T, e)
  reward = reward / nSim
  rew.append(reward)
print(rew)

plt.plot(rangeEpsilon, rew);
