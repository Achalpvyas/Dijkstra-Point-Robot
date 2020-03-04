from node import Node
from collections import deque
import numpy as np
import math


######################################
#          Workspace=
######################################
def isValidWorkspace(pt,r = 3): #To be modified
    circle = (pt[0] - math.floor(225/r))**2 + (pt[1]-math.floor(150/r))**2 
    ellipse = (pt[0] - math.floor(225/r))**2/40**2 + (pt[1]-math.floor(150/r))**2/25**2
    if(circle <= math.floor(25/r)**2 or ellipse<= 1):
        return False
    return True


# checks whether next action is near an obstacle or ill defined 
def isSafe(newState,r=3):
    col = math.floor(300/r)
    row = math.floor(200/r)

    if(newState[0]< 0 or newState[0]>row or newState[1]<0 or newState[1]>col):
        return False
    return isValidWorkspace(newState,r)

#prints solution path 
def printPath(node):
    l = []
    current = node
    while(current):
       l.append(current.state)
       current = current.parent
    return l



#generates optimal path for robot
def generatePath(q,A,startPosition,goalPosition,costIncrement,nodesExplored,res=3):
    key = str(startPosition[0]) + str(startPosition[1])
    root = Node(startPosition,0.0,None)
    nodesExplored[key] = root
    q.appendleft(root)
    
    while(len(q)>0):
        currentNode = q.pop()
        if((currentNode.state == goalPosition).all()):
            sol = printPath(currentNode)
            return [True,sol]

        for i in range(8): 
            newState = A[i,:] + currentNode.state 
            s = str(newState[0])+str(newState[1])

            if(s not in nodesExplored):
                if(isSafe(newState,res)):
                    newCost = currentNode.cost + costIncrement[i]
                    newNode = Node(newState,newCost,currentNode)
                    nodesExplored[s] = newNode
                    q.appendleft(newNode)

            else:
                if(nodesExplored[s].cost > currentNode.cost + costIncrement[i]):
                    nodesExplored[s].cost = currentNode.cost + costIncrement[i]
                    nodesExplored[s].parent = currentNode
    return  [False,None] 


if __name__ == "__main__":
    #action set
    A = np.array([[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]])
    costIncrement = [1.0,1.0,1.0,1.0,math.sqrt(2),math.sqrt(2),math.sqrt(2),math.sqrt(2)]

    nodesExplored = {}
    q = deque()
    startPosition = np.array([12,2])
    goalPosition = np.array([5,5])
    print(generatePath(q,A,startPosition,goalPosition,costIncrement,nodesExplored))
    


