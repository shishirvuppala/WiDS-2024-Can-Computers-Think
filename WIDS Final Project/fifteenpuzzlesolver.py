#PLAN
#1.) 3 subparts 1.)first row 2.)second row 3.) rest
#2.) need hasher for each done
#3.) need statespace generator for each done

import pickle
import os
import numpy as np
import time
from tabulate import tabulate

def hash1(arr):
    s = []
    for i in range(4):
        for j in range(4):
            c = arr[i][j]
            if c not in [1,2,3,4,16]:
                c = 0
            s.append(c)
    return s

def hash2(arr):
    s = []
    for i in '1234':
        s.append(-1)
    for i in range(1,4):
        for j in range(4):
            c = arr[i][j]
            if c not in [5,6,7,8,16]:
                c = 0
            s.append(c)
    return s

def hash3(arr):
    s = []
    for i in '12345678':
        s.append(-1)
    for i in range(2,4):
        for j in range(4):
            s.append(arr[i][j])
    return s

def generator(ar,length,numarleft,zeroleft,state,maxlength):
    if(length == maxlength):
        state.append(ar.copy())
    else:
        for i in range(len(numarleft)):
            c = numarleft[i]
            numarleft.pop(i)
            ar.append(c)
            generator(ar,length+1,numarleft,zeroleft,state,maxlength)
            numarleft.insert(i,c)
            ar.pop()
        if(zeroleft > 0):
            ar.append(0)
            zeroleft = zeroleft - 1
            generator(ar,length+1,numarleft,zeroleft,state,maxlength)
            zeroleft = zeroleft + 1
            ar.pop()


#process

def is_goal_state(ar):
    if ( ar[:4] == [1,2,3,4] and ar.count(16) == 1 and ar.count(0) == 11):
        return True
    if ( ar[:8] == [-1,-1,-1,-1,5,6,7,8] and ar.count(16) == 1 and ar.count(0) == 7):
        return True
    if (ar == [-1,-1,-1,-1,-1,-1,-1,-1,9,10,11,12,13,14,15,16]):
        return True
    return False

gamma = 0.8
def reward(ar):
    if is_goal_state(ar):
        return 500
    return -1

def improvement(V,Policy,states):
    Policystable = True
    for state in states:
        prevac = Policy[tuple(state)]
        if is_goal_state(state):
            continue
        i = state.index(16)
        maxVal = -float('inf')
        action = ''
        if(i//4 != 0 and state[i-4] != -1): # up
            ar = state.copy()
            ar[i-4],ar[i] = ar[i],ar[i-4]
            upval = reward(ar) + gamma * V[tuple(ar)]
            if(upval > maxVal):
                maxVal = upval
                action = 'u'
        if(i//4 != 3 and state[i+4] != -1): # down
            ar = state.copy()
            ar[i+4],ar[i] = ar[i],ar[i+4]
            downval = reward(ar) + gamma * V[tuple(ar)]
            if(downval > maxVal):
                maxVal = downval
                action = 'd'
        if(i%4 != 3 and state[i+1] != -1): # right
            ar = state.copy()
            ar[i+1],ar[i] = ar[i],ar[i+1]
            rightval = reward(ar) + gamma * V[tuple(ar)]
            if(rightval > maxVal):
                maxVal = rightval
                action = 'r'
        if(i%4 != 0 and state[i-1] != -1): # left
            ar = state.copy()
            ar[i-1],ar[i] = ar[i],ar[i-1]
            leftval = reward(ar) + gamma * V[tuple(ar)]
            if(leftval > maxVal):
                maxVal = leftval
                action = 'l'
        if action != prevac:
            Policystable  = False
        Policy[tuple(state)] = action
    return Policystable


def evaluate(V,Policy,states):
    for state in states:
        if is_goal_state(state):
            continue
        action = Policy[tuple(state)]
        ar = state.copy()
        i = state.index(16)
        if (action == "u" ) :
            ar[i],ar[i-4] = ar[i-4],ar[i]
        elif (action == 'd'):
            ar[i],ar[i+4] = ar[i+4],ar[i]
        elif (action == 'r'):
            ar[i],ar[i+1] = ar[i+1],ar[i]
        else:
            ar[i],ar[i-1] = ar[i-1],ar[i]
        V[tuple(state)] = reward(ar) + gamma * V[tuple(ar)]

#subpart 1
stateSpace1 = []
generator([],0,[1,2,3,4,16],11,stateSpace1,16)

V1 = {}
Policy1 = {}

for i in stateSpace1:
    j = tuple(i)
    V1[j] = 0
    Policy1[j] = None


#subpart 2
stateSpace2 = []
generator([-1,-1,-1,-1],4,[5,6,7,8,16],7,stateSpace2,16)

V2 = {}
Policy2 = {}

for i in stateSpace2:
    j = tuple(i)
    V2[j] = 0
    Policy2[j] = None

#subpart 3
stateSpace3 = []
generator([-1,-1,-1,-1,-1,-1,-1,-1],8,[9,10,11,12,13,14,15,16],0,stateSpace3,16)

V3 = {}
Policy3 = {}

for i in stateSpace3:
    j = tuple(i)
    V3[j] = 0
    Policy3[j] = None

#final finder PROBLEM

def find16(arr):
    for i in range(4):
        for j in range(4):
            if(arr[i][j] == 16):
                return i,j

def up(arr):
    row, col = find16(arr)
    arr[row][col],arr[row-1][col] = arr[row-1][col],arr[row][col]

def down(arr):
    row, col = find16(arr)
    arr[row][col],arr[row+1][col] = arr[row+1][col],arr[row][col]

def right(arr):
    row, col = find16(arr)
    arr[row][col],arr[row][col+1] = arr[row][col+1],arr[row][col]

def left(arr):
    row, col = find16(arr)
    arr[row][col],arr[row][col-1] = arr[row][col-1],arr[row][col]


def solver(tobesolved,inputsarray):
    while(1):
        if(len(inputsarray) > 150):
            inputsarray = [2025,]
            return False
            break
        x = hash1(tobesolved)
        act = Policy1[tuple(x)]
        if act == 'u':
            up(tobesolved)
            inputsarray.append('u')
        elif act == 'd':
            down(tobesolved)
            inputsarray.append('d')
        elif(act == 'r'):
            right(tobesolved)
            inputsarray.append('r')
        elif(act == 'l'):
            left(tobesolved)
            inputsarray.append('l')
        else:
            break
    while(1):
        x = hash2(tobesolved)
        act = Policy2[tuple(x)]
        if(len(inputsarray) > 150):
            inputsarray = [2025,]
            return False
            break
        if(act == 'u'):
            up(tobesolved)
            inputsarray.append('u')
        elif act == 'd':
            down(tobesolved)
            inputsarray.append('d')
        elif(act == 'r'):
            right(tobesolved)
            inputsarray.append('r')
        elif(act == 'l'):
            left(tobesolved)
            inputsarray.append('l')
        else:
            break
    while(1):
        x = hash3(tobesolved)
        act = Policy3[tuple(x)]
        if(len(inputsarray) > 150):
            inputsarray = [2025,]
            return False
            break
        if act == 'u':
            up(tobesolved)
            inputsarray.append('u')
        elif act == 'd':
            down(tobesolved)
            inputsarray.append('d')
        elif(act == 'r'):
            right(tobesolved)
            inputsarray.append('r')
        elif(act == 'l'):
            left(tobesolved)
            inputsarray.append('l')
        else:
            break
    return True

#PolicyLoader

def getPolicy(policy,filename,v,states):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            loaded_policy = pickle.load(file)
            policy.clear()
            policy.update(loaded_policy)
    else:
        improvement(v,policy,states)
        while(1):
            evaluate(v,policy,states)
            stable = improvement(v,policy,states)
            if stable:
                break
        with open(filename, 'wb') as file:
            pickle.dump(policy,file)

getPolicy(Policy1,"Phase1Solver.txt",V1,stateSpace1)

getPolicy(Policy2,"Phase2Solver.txt",V2,stateSpace2)

getPolicy(Policy3,"Phase3Solver.txt",V3,stateSpace3)





# This is the 15 puzzle we are solving
x = [[11,15,12,3],
    [2,13,10,5],
    [1,7,4,8],
    [6,16,9,14]]
x = np.array(x)


if __name__ == "__main__":
    howtosolve = []
    y = np.where(x==16,'',x)
    print(tabulate(y,tablefmt="grid"))
    print("Solving")
    ar = x.tolist()
    boole = solver(ar,howtosolve)
    if(not boole):
        print("Unsolvable 15 puzzle")
    else:
        T = 0
        for action in howtosolve:
            time.sleep(0.9)
            T = T + 1
            if (action == 'u'):
                up(x)
                y = np.where(x==16,'',x)
                print(tabulate(y,tablefmt="grid"))
            if (action == 'd'):
                down(x)
                y = np.where(x==16,'',x)
                print(tabulate(y,tablefmt="grid"))
            if (action == 'r'):
                right(x)
                y = np.where(x==16,'',x)
                print(tabulate(y,tablefmt="grid"))
            if(action == 'l'):
                left(x)
                y = np.where(x==16,'',x)
                print(tabulate(y,tablefmt="grid"))
            print("T = ",T)
    
