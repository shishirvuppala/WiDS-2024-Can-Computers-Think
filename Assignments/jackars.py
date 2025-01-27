import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.special import factorial

stateSpace = [(i,j) for i in range(21) for j in range(21)]

gamma = 0.9
MaxCars = 20
MaxMove = 5 
cost = 2
gain = 10

V = np.zeros((21,21))
Policy = np.zeros((21,21))


vals = np.array(range(21))
prob2 = math.exp(-2) * (2 ** vals /factorial(vals))
prob3 = math.exp(-3) * (3 ** vals /factorial(vals))
prob4 = math.exp(-4) * (4 ** vals /factorial(vals))

def expected_reward(state,action):
    exprew = 0
    n1 = int(state[0] + action)
    n2 = int(state[1] - action)
    p1,p2,p3,p4 = 0,0,0,0
    for ic1 in range(0,n1+1):
        if (ic1 < n1):
            p1 = prob3[ic1]
        else:
            p1 = 1 - np.sum(prob3[:n1])
        for ic2 in range(0,n2+1):
            if (ic2 < n2):
                p2 = prob4[ic2]
            else:
                p2 = 1 - np.sum(prob4[:n2])
            rew = (ic1+ic2)*10 - 2 * abs(action) 
            for rc1 in range(0,21-(n1-ic1)):
                if (rc1 < 20-(n1-ic1)):
                    p3 = prob3[rc1]
                else:
                    p3 = 1 - np.sum(prob3[:(20-(n1-ic1))])
                for rc2 in range(0,21-(n2-ic2)):
                    if (rc2 < 20-(n2-ic2)):
                        p4 = prob2[rc2]
                    else:
                        p4 = 1 - np.sum(prob2[:(20-(n2-ic2))])
                    n1f = n1 - ic1 + rc1
                    n2f = n2 - ic2 + rc2
                    exprew = exprew + (p1*p2*p3*p4) * (rew + gamma * V[n1f][n2f])
    return exprew

def improvement():
    PolicyStable = True
    for state in stateSpace:
        n1 = state[0]
        n2 = state[1]
        prevact = Policy[n1][n2]
        maxe = -float('inf')
        prefact = 0
        for action in range(-min(min(n1,5),min(20-n2,5)),min(min(n2,5),min(20-n1,5))+1):
            rew = expected_reward(state,action)
            if(rew > maxe):
                maxe = rew
                prefact = action
        Policy[n1][n2] = prefact
        if(prevact != prefact):
            PolicyStable = False
    return PolicyStable

def evaluation():
    the = 0.1
    while(1): 
        delta = 0
        for state in stateSpace:
            n1 = state[0]
            n2 = state[1]
            action = Policy[n1,n2]
            newV = expected_reward(state,action)
            delta = max(delta,abs(newV - V[n1][n2]))
            V[n1][n2] = newV
        if(delta < the):
            break

def heatmapmaker():
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(21), labels = np.arange(21))
    ax.set_yticks(np.arange(21), labels = np.arange(21))
    im = ax.imshow(Policy,origin='lower')
    fig.colorbar(im)
    ax.set_title("HeatMap of the policy")
    plt.show()

def main():
    while(1):
        evaluation()
        stable = improvement()
        if stable:
            break
    heatmapmaker()

main()