import pygame
import numpy as np
from dijkstra_point_rigid import *



###################################################
#                  Parameters 
###################################################
A = np.array([[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]])
costIncrement = [1.0,1.0,1.0,1.0,math.sqrt(2),math.sqrt(2),math.sqrt(2),math.sqrt(2)]

clearance = radius = 0

print('Enter Type of robot\n 1 -> point robot \n 2 -> rigid robot \
        \n Enter number :')

robotType = int(input())

if(robotType == 2):
    print("Enter cleareance")
    clearance = int(input())
    print("Enter radius")
    radius = int(input())

print('Enter start location s1')
s1 = int(input())
print('Enter start location s2')
s2 = 200-int(input())

print('Enter goal location g1')
g1 = int(input())
print('Enter goal location g2')
g2 = 200-int(input())

res = 2 #resolution of grid
scale = 3 #scale of grid

startPosition = np.round((np.array([s1,s2]))/res)
goalPosition = np.round((np.array([g1,g2]))/res)

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

size_x = math.ceil(300)
size_y = math.ceil(200)
gameDisplay = pygame.display.set_mode((size_x*scale,size_y*scale))


############################################################
#                Display Obstacles
############################################################
circlePts = [225,50,25]

polygonPts =  np.array([[20,120],[25,185],[75,185],[100,150],[75,120],[50,150]])
polygonPts[:,1] = (size_y - polygonPts[:,1])

rhombusPts = np.array([[225,10],[200,25],[225,40],[250,25]])
rhombusPts[:,1] = (size_y - rhombusPts[:,1])

ellipsePts = np.array([110,80,80,40])


X =           np.array([95+10*math.cos(math.radians(60)), 95-75*math.cos(math.radians(30))+10*math.cos(math.radians(60)), 95-75*math.cos(math.radians(30)), 95])
Y = size_y -  np.array([30+10*math.sin(math.radians(60)), 30+75*math.sin(math.radians(30))+10*math.sin(math.radians(60)), 30+75*math.sin(math.radians(30)), 30])
rectPts = np.column_stack((X,Y))

pygame.draw.circle(gameDisplay, red, (circlePts[0]*scale,circlePts[1]*scale), circlePts[2]*scale)
pygame.draw.polygon(gameDisplay,red,scale*polygonPts)
pygame.draw.polygon(gameDisplay,red,scale*rhombusPts)
pygame.draw.ellipse(gameDisplay,red,scale*ellipsePts)
pygame.draw.polygon(gameDisplay,red,scale*rectPts)



############################################################
#          Draw Explored Nodes and solution path
############################################################
nodesExplored = {}
# q = deque()
# q = PriorityQueue()
q = []

if(not isSafe(startPosition,res,clearance + radius) or not isSafe(goalPosition,res,clearance+radius)):
    basicfont = pygame.font.SysFont(None, 48)
    text = basicfont.render('Start or goal position must be in a valid workspace', True, (255, 0, 0), (255, 255, 255))
    textrect = text.get_rect()
    textrect.centerx = gameDisplay.get_rect().centerx
    textrect.centery = gameDisplay.get_rect().centery
 
    gameDisplay.blit(text, textrect)
    pygame.display.update()
    pygame.time.delay(2000)

else:
    success,solution = generatePath(q,A,startPosition,goalPosition,costIncrement,nodesExplored,res,clearance+radius)

    #############################################
    #     Drawing 
    #############################################
    if(success):
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
            pygame.time.delay(2000)
            draw = False
    else:
        basicfont = pygame.font.SysFont(None, 48)
        text = basicfont.render('Path can\'t be generated', True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = gameDisplay.get_rect().centerx
        textrect.centery = gameDisplay.get_rect().centery
     
        gameDisplay.blit(text, textrect)
        pygame.display.update()
        pygame.time.delay(2000)

pygame.quit()

