from __future__ import print_function

import pygame, sys, time, random
from pygame.locals import *

from pygame import pyganim


# Set up pygame
pygame.init()

gScreen = None


# Set up the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (23, 33, 199)

# Window dimensions
WINDOW_X = 700
WINDOW_Y = 500

# Size of each grid cell
GRID_X = 10
GRID_Y = 10

# Max dimensions of grid
MAX_CELL_POSX = WINDOW_X // GRID_X
MAX_CELL_POSY = WINDOW_Y // GRID_Y



class CellGrid(object):
   '''A grid of Cell objects'''
   
   def __init__(self, sizex, sizey):
      # Each row is a list of Cell objects
      self.oRows = []
      for j in range(sizey):
         # Create a row of cells
         row = [Cell(i, j) for i in range(sizex)] 
         self.oRows.append(row)
      
   def getCell(self, x, y):
      return self.oRows[y][x]

   def getRandomCell(self):
      return self.oRows[random.randint(0, MAX_CELL_POSY-1)][random.randint(0, MAX_CELL_POSX-1)]
      
   def drawCells(self):
      for rowIdx in range(len(self.oRows)):
         for colIdx in range(MAX_CELL_POSX):
            self.oRows[rowIdx][colIdx].draw()
      
      
class Cell(object):
   def __init__(self, x, y):
      self.oPosX = x
      self.oPosY = y
      
      # Public
      self.State = 0
      self.StateSwitchCount = 0
      
   def __str__(self):
      return "cell: %d, %d is: %s" % (self.oPosX, self.oPosY, 'dead' if self.State == 0 else 'alive')
      
   def toggleState(self):
      self.State = 1 if self.State == 0 else 0
      self.StateSwitchCount += 1
      
   def draw(self):
      '''Calculate the position of the cell in pixels & draw it'''
      if self.State == 1:
         if self.StateSwitchCount == 1:
            dcolor = BLUE 
         elif self.StateSwitchCount == 2:
            dcolor = (23, 188, 45)
         elif self.StateSwitchCount == 3:
            dcolor = (198, 18, 55)
         else:
            dcolor = (156, 128, 200)
      elif self.State == 0:
         dcolor = WHITE
         
      #if self.State == 1:
      pygame.draw.rect(gScreen, dcolor, [self.oPosX * GRID_X + 1, self.oPosY * GRID_Y + 1, GRID_X-1, GRID_Y-1])
      

def drawFrame(drawList):
   for drawable in drawList:
      drawable.draw()


def drawGrid():
   '''Draw the background grid'''
   greyCol = (245, 241, 232)
   for i in range(10, WINDOW_X, 10):
      pygame.draw.line(gScreen, greyCol, (i, 0),  (i, WINDOW_Y))
   
   for i in range(10, WINDOW_Y, 10):
      pygame.draw.line(gScreen, greyCol, (0, i),  (WINDOW_X, i))

   
def main():
   # Set up the window
   global gScreen
   gScreen = pygame.display.set_mode((WINDOW_X, WINDOW_Y), 0, 32)
   pygame.display.set_caption('Game of Life')

   # Create the game clock
   clock = pygame.time.Clock()
   done = False
   
   previousGenCellGrid = CellGrid(MAX_CELL_POSX, MAX_CELL_POSY)
   currGenCellGrid = CellGrid(MAX_CELL_POSX, MAX_CELL_POSY)
   

   lastFrameSecs = 0.0
   drawList = []
   
   gScreen.fill(WHITE)
   
   # run the game loop
   while not  done:

      for event in pygame.event.get():
         if event.type == QUIT:
            done = True
            break


      frameMilli = clock.tick(60)               # milliseconds passed since last frame
      frameSeconds = frameMilli / 1000.0        # fractional seconds passed since last frame  
      
      
      #gScreen.fill(WHITE)
      
      drawGrid()
      #drawFrame(drawList)


      
      lastFrameSecs += frameSeconds
      if lastFrameSecs >= 0.10: #825:
         currGenCellGrid.getRandomCell().toggleState()
         currGenCellGrid.drawCells()
         lastFrameSecs = 0.0
      
      pygame.display.flip()   
     
      

   pygame.quit()


main()


