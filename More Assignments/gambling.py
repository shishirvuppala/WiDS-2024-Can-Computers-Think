import numpy as np
import matplotlib.pyplot as plt

V = np.zeros(101)
Policy = np.zeros(101)
Ph = 0.4

reward = np.zeros(101)
reward[100] = 1

def improvement():
    for i in range(1,100):
        m = -1
        prefact = 0
        for action in range(1,min(i,100-i)+1):
            p = int(action + i)
            d = int(i-action)
            temp = Ph*(V[p]+reward[p]) + (1-Ph)*(V[d]+reward[d])
            if(temp - m > 0.00001):
                prefact = action
                m = temp
        Policy[i] = prefact

def evaluation():
    newV = np.zeros(101)
    m = 0
    global V
    for i in range(1,100):
        act = Policy[i]
        p = int(act + i)
        d = int(i-act)
        temp = Ph*(V[p]+reward[p]) + (1-Ph)*(V[d]+reward[d])
        m = max(m,abs(V[i]-temp))
        newV[i] = temp
    V = newV
    return m

def main():
    delta = 0.0001
    while(1):
        improvement()
        m = evaluation()
        if(m<delta):
            break
    x_positions = range(101)
    plt.bar(x_positions, Policy, width=0.9, color='skyblue', edgecolor='black')
    plt.xlabel('Capital')
    plt.ylabel('Final Policy')
    plt.show()

main()