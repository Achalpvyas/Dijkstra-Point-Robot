from node import Node
from collections import deque
import numpy as np
import math



# checks whether next action is near an obstacle or ill defined 
def isSafe(newState):
    return True


def printPath(node):
    pass


#generates optimal path for robot
def generatePath(q,visited,A,startPosition,goalPosition,costIncrement,nodesExplored):
    key = str(startPosition[0]) + str(startPosition[1])
    root = Node(startPosition,0.0,None)
    nodesExplored[key] = root
    visited.add(key)
    q.appendleft(root)
    
    while(len(q)>0):
        currentNode = q.pop()
        if((currentNode.state == goalPosition).all()):
            printPath(currentNode)
            break
           
        for i in range(8): 
            newState = A[i,:] + currentNode.state 
            s = str(newState[0])+str(newState[1])

            if(s not in visited and isSafe(newState)):
                visited.add(s)
                newCost = currentNode.cost + costIncrement[i]
                newNode = Node(newState,newCost,Node)
                nodesExplored[s] = newNode
                q.append(newNode)

            else:
                if(nodesExplored[s].cost > currentNode.cost + costIncrement[i]):
                    nodesExplored[s].cost = currentNode.cost + costIncrement[i]
                    nodesExplored[s].parent = currentNode

    return False


if __name__ == "__main__":
    #action set
    A = np.array([[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]])
    costIncrement = [1.0,1.0,1.0,1.0,math.sqrt(2),math.sqrt(2),math.sqrt(2),math.sqrt(2)]

    visited = set()
    nodesExplored = {}
    q = deque()
    startPosition = np.array([0,0])
    goalPosition = np.array([5,5])
    generatePath(q,visited,A,startPosition,goalPosition,costIncrement,nodesExplored)


