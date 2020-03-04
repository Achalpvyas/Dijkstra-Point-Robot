import pygame
import numpy as np
from dijkstra_point import *




#################################
#  Board parameters
#################################
pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


res = 3 #resolution of grid
scale = 3 #scale of grid

size_x = math.ceil(300)
size_y = math.ceil(200)
gameDisplay = pygame.display.set_mode((size_x*scale,size_y*scale))


#####################################
#       Display Obstacles
#####################################
circlePts = [255,50,25]

polygonPts =  np.array([[20,120],[25,185],[75,185],[100,150],[75,120],[50,150],[20,120]])
polygonPts[:,1] = (size_y - polygonPts[:,1])

rhombusPts = np.array([[225,10],[200,25],[225,40],[250,25]])
rhombusPts[:,1] = (size_y - rhombusPts[:,1])

ellipsePts = np.array([120,80,80,40])

rectPts = np.array([[95,30],[20,30],[20,40],[95,40]])
rectPts[:,1] = (size_y - rectPts[:,1]) #To be modified

pygame.draw.circle(gameDisplay, red, (circlePts[0]*scale,circlePts[1]*scale), circlePts[2]*scale)
pygame.draw.polygon(gameDisplay,red,scale*polygonPts)
pygame.draw.polygon(gameDisplay,red,scale*rhombusPts)
pygame.draw.polygon(gameDisplay,red,scale*rectPts)
pygame.draw.ellipse(gameDisplay,red,scale*ellipsePts)
pygame.display.flip()


##############################################
#     Explore Nodes
##############################################
A = np.array([[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]])
costIncrement = [1.0,1.0,1.0,1.0,math.sqrt(2),math.sqrt(2),math.sqrt(2),math.sqrt(2)]

s1 = 0
s2 = 0
g1 = 50
g2 = 140

nodesExplored = {}
q = deque()
startPosition = np.round((np.array([s1,s2]))/res)
goalPosition = np.round((np.array([g1,g2]))/res)

if(not isSafe(startPosition) and not isSafe(goalPosition)):
    print("Start or goal position must be in a valid workspace")

else:
    success,solution = generatePath(q,A,startPosition,goalPosition,costIncrement,nodesExplored)


    #############################################
    #     Drawing 
    #############################################
    draw = True
    while draw:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #draw nodesExplored
        for s in nodesExplored:
            pt = nodesExplored[s].state
            x,y = pt*scale*res

            #draw explored nodes
            pygame.draw.rect(gameDisplay,white,(x,y,res*scale,res*scale))

            #draw start and goal locations
            pygame.draw.rect(gameDisplay,blue,(startPosition[0]*res*scale,startPosition[1]*res*scale,res*scale,res*scale))
            pygame.draw.rect(gameDisplay,blue,(goalPosition[0]*res*scale,goalPosition[1]*res*scale,res*scale,res*scale))
            pygame.display.flip()
       

        # draw solution path
        for i in range(len(solution)-1,-1,-1):
            pt = solution[i]
            x,y = pt*scale*res
            pygame.draw.rect(gameDisplay,green,(x,y,res*scale,res*scale))
            pygame.display.flip()
        pygame.time.delay(1000)
        draw = False
    pygame.quit()


