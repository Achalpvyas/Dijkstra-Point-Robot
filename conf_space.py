import pygame
import numpy as np


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

gameDisplay = pygame.display.set_mode((300*scale,200*scale))


#####################################
#       Display Obstacles
#####################################
circlePts = [255,50,25]

polygonPts =  np.array([[20,120],[25,185],[75,185],[100,150],[75,120],[50,150],[20,120]])
polygonPts[:,1] = (200 - polygonPts[:,1])

rhombusPts = np.array([[225,10],[200,25],[225,40],[250,25]])
rhombusPts[:,1] = (200 - rhombusPts[:,1])

ellipsePts = np.array([120,80,80,40])

rectPts = np.array([[95,30],[20,30],[20,40],[95,40]])
rectPts[:,1] = (200 - rectPts[:,1]) #To be modified


pygame.draw.circle(gameDisplay, red, (circlePts[0]*scale,circlePts[1]*scale), circlePts[2]*scale)
pygame.draw.polygon(gameDisplay,red,scale*polygonPts)
pygame.draw.polygon(gameDisplay,red,scale*rhombusPts)
pygame.draw.polygon(gameDisplay,red,scale*rectPts)
pygame.draw.ellipse(gameDisplay,red,scale*ellipsePts)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
