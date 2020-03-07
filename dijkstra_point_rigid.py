from node import Node
from collections import deque
from queue import PriorityQueue
import heapq
import numpy as np
import math

######################################
#          Workspace
######################################
def isValidWorkspace(pt,r = 3,radiusClearance=0): #To be modified
    x,y = pt
   
    #------------------------------------------------------------------------------
    #                              Circle pts
    #------------------------------------------------------------------------------
    ptInCircle = (x - math.floor(225/r))**2 + (y -math.floor(50/r))**2 - math.floor((25+radiusClearance)/r)**2 <= 0
 
    #--------------------------------------------------------------------------------
    #                             ellipse pts
    #--------------------------------------------------------------------------------
    ptInEllipse =((x - math.floor(150/r))/math.floor((40+radiusClearance)/r))**2 + ((y-math.floor(100/r))/math.floor((20+radiusClearance)/r))**2 <= 1
   
    #---------------------------------------------------------------------------------
    # Non Convex Polygon pts -- Partition nonconvex polygon into two convex regions
    #---------------------------------------------------------------------------------
    X =         np.array([50,75,100,75,25,20,50])/r
    Y = 200/r - np.array([150,120,150,185,185,120,150])/r
    nonConvexRegion1 = (y-Y[0]) <= ((Y[1]-Y[0])/(X[1]-X[0]))*(x-X[0]) +                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[1]-Y[0])/(X[1]-X[0]))**2))   and \
                       (y-Y[1]) <= ((Y[2]-Y[1])/(X[2]-X[1]))*(x-X[1]) +                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[2]-Y[1])/(X[2]-X[1]))**2))   and \
                       (y-Y[2]) >= ((Y[3]-Y[2])/(X[3]-X[2]))*(x-X[2]) -                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[3]-Y[2])/(X[3]-X[2]))**2))   and \
                       (y-Y[3]) >= ((Y[0]-Y[3])/(X[0]-X[3]))*(x-X[3])                                    

    nonConvexRegion2 = (y-Y[3]) >= ((Y[4]-Y[3])/(X[4]-X[3]))*(x-X[3]) -                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[4]-Y[3])/(X[4]-X[3]))**2))   and \
                       (y-Y[4]) >= ((Y[5]-Y[4])/(X[5]-X[4]))*(x-X[4]) -                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[5]-Y[4])/(X[5]-X[4]))**2))   and \
                       (y-Y[5]) <= ((Y[6]-Y[5])/(X[6]-X[5]))*(x-X[5]) +                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[6]-Y[5])/(X[6]-X[5]))**2))   and \
                       (y-Y[6]) <= ((Y[3]-Y[6])/(X[3]-X[6]))*(x-X[6]) +                                   \
                                    radiusClearance/r * (1+math.sqrt(((Y[3]-Y[6])/(X[3]-X[6]))**2))   


    ptInNonConvex = nonConvexRegion1 or nonConvexRegion2

    #--------------------------------------------------------------------------------
    #                             Rhombus pts
    #--------------------------------------------------------------------------------
    X = np.array([225,200,225,250])/r
    Y = 200/r - np.array([40,25,10,25])/r
    ptInRhombus =  (y-Y[0]) >= ((Y[1]-Y[0])/(X[1]-X[0]))*(x-X[0]) -                                   \
                                radiusClearance/r * (1+math.sqrt(((Y[1]-Y[0])/(X[1]-X[0]))**2))   and \
                   (y-Y[1]) <= ((Y[2]-Y[1])/(X[2]-X[1]))*(x-X[1]) +                                   \
                                radiusClearance/r * (1+math.sqrt(((Y[2]-Y[1])/(X[2]-X[1]))**2))   and \
                   (y-Y[2]) <= ((Y[3]-Y[2])/(X[3]-X[2]))*(x-X[2]) +                                   \
                                radiusClearance/r * (1+math.sqrt(((Y[3]-Y[2])/(X[3]-X[2]))**2))   and \
                   (y-Y[3]) >= ((Y[0]-Y[3])/(X[0]-X[3]))*(x-X[3]) -                                   \
                                radiusClearance/r * (1+math.sqrt(((Y[0]-Y[3])/(X[0]-X[3]))**2))   
 

    #--------------------------------------------------------------------------------
    #                         Tilted Rectangle pts 
    #--------------------------------------------------------------------------------
    X =          np.array([95+10*math.cos(math.radians(60)), 95-75*math.cos(math.radians(30))+10*math.cos(math.radians(60)), 
                           95-75*math.cos(math.radians(30)), 95])/r
    Y = 200/r -  np.array([30+10*math.sin(math.radians(60)), 30+75*math.sin(math.radians(30))+10*math.sin(math.radians(60)), 
                           30+75*math.sin(math.radians(30)), 30])/r

    ptInRectangle = (y-Y[0]) >= ((Y[1]-Y[0])/(X[1]-X[0]))*(x-X[0]) -                                   \
                                 radiusClearance/r * (1+math.sqrt(((Y[1]-Y[0])/(X[1]-X[0]))**2))   and \
                    (y-Y[1]) >= ((Y[2]-Y[1])/(X[2]-X[1]))*(x-X[1]) -                                   \
                                 radiusClearance/r * (1+math.sqrt(((Y[2]-Y[1])/(X[2]-X[1]))**2))   and \
                    (y-Y[2]) <= ((Y[3]-Y[2])/(X[3]-X[2]))*(x-X[2]) +                                   \
                                 radiusClearance/r * (1+math.sqrt(((Y[3]-Y[2])/(X[3]-X[2]))**2))   and \
                    (y-Y[3]) <= ((Y[0]-Y[3])/(X[0]-X[3]))*(x-X[3]) +                                   \
                                 radiusClearance/r * (1+math.sqrt(((Y[0]-Y[3])/(X[0]-X[3]))**2))   

    if(ptInCircle  or ptInEllipse  or ptInNonConvex or ptInRhombus or ptInRectangle):
        return False
    return True


# checks whether next action is near an obstacle or ill defined 
def isSafe(newState,r=3,radiusClearance = 0):
    col = math.floor(300/r)
    row = math.floor(200/r)

    if(newState[0]< 0 or newState[0]>col or newState[1]<0 or newState[1]>row):
        return False
    return isValidWorkspace(newState,r,radiusClearance)

#prints solution path 
def printPath(node):
    l = []
    current = node
    while(current):
       l.append(current.state)
       current = current.parent
    return l

#generates optimal path for robot
def generatePath(q,A,startPosition,goalPosition,costIncrement,nodesExplored,res=3,radiusClearance=0):
    key = str(startPosition[0]) + str(startPosition[1])
    root = Node(startPosition,0.0,None)
    nodesExplored[key] = root

    # q.appendleft(root)
    # q.put(root)
    count = 1
    heapq.heappush(q,(root.cost,count,root))
     
    while(len(q)>0):
        # currentNode = q.pop()
        # currentNode = q.get()
        _,_,currentNode = heapq.heappop(q)

        if((currentNode.state == goalPosition).all()):
            sol = printPath(currentNode)
            return [True,sol]
        
        for i in range(8): 
            newState = A[i,:] + currentNode.state 
            s = str(newState[0])+str(newState[1])

            if(s not in nodesExplored):
                if(isSafe(newState,res,radiusClearance)):
                    newCost = currentNode.cost + costIncrement[i]
                    newNode = Node(newState,newCost,currentNode)
                    nodesExplored[s] = newNode

                    # q.appendleft(newNode)
                    # q.put(newNode)
                    heapq.heappush(q,(newNode.cost,count,newNode))
                    count += 1

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
    # q = deque()
    # q = PriorityQueue()
    q = []
    startPosition = np.array([0,0])
    goalPosition = np.array([250,140])
    print(generatePath(q,A,startPosition,goalPosition,costIncrement,nodesExplored,4))
    

