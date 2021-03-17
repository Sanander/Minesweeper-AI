# -*- coding: utf-8 -*-
"""Minesweeper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fJdwJmyo1QVDK6sWse6uoD8zHXg-u_2C
"""

import random
import queue
import math

class Square:

  def __init__(self, row=0, col=0, mine=False, clue=0, minesAround=0, safeAround=0, hiddenAround=0, visible=None):  

    self.row=row
    self.col=col
    self.mine = mine
    self.clue = clue
    self.minesAround=minesAround
    self.safeAround=safeAround
    self.hiddenAround=hiddenAround
    self.visible = visible

  def getMine(self):
    return self.mine

  def setMine(self, mine=True):
    self.mine = mine
    return

  def getProximity(self):
    return self.proximity

  def setProximity(self, proximity):
    self.proximity = proximity
    return

  def getVisible(self):
    return self.visible

  def setVisible(self, visible):
    self.visible = visible
    return

  def __str__(self):
    if self.visible == None:
      return "-"
    if not self.getVisible():
      return str(self.proximity)
    if self.getMine():
      return "M"
    return str(self.proximity)

#Creates board
def generateBoard(d, n):
  board = [[Square() for x in range(d)] for x in range(d)]
  
  x = 0
  while (n > x):
    i = random.randint(0, d-1)
    j = random.randint(0, d-1)
    if (board[i][j].getMine() == False):
        board[i][j].setMine(True)
        x+=1
  
  for i in range(d):
     for j in range(d):
       board[i][j].setProximity(checkSurrounding(board, i, j))

  return board

#Get info on neigbors
def checkSurrounding(board, i, j):
  clue = 0
  visibleMineCount=0
  visibleSafeSpace=0
  neighbors=0
  for x in range(i-1, i+2):
    for y in range(j-1, j+2):
      if (x >= 0 and y >= 0):
        if (x < len(board) and y < len(board)):
            neighbors=neighbors+1
            if (board[x][y].getMine()):
                clue += 1
                if(board[x][y].getVisible==True):
                    visibleMineCount=visibleMineCount+1
            elif (board[x][y].getVisible==True):
                    visibleSafeSpace=visibleSafeSpace+1
  return (clue,neighbors,visibleMineCount,visibleSafeSpace)

#Display board
def printBoard(board):
  for x in range(len(board)):
     for y in range(len(board)):
       print(str(board[x][y]), end=" ")
     print("\n")

#Print hidden neigbors
def getNewNeighbors(board, i, j):
  ret = []
  
  for x in range(i-1, i+2):
    for y in range(j-1, j+2):
      if (x != i or y != j):
        if (x >= 0 and y >= 0):
          if (x < len(board) and y < len(board)):
            if (board[x][y].getVisible() == None):
              ret.append((x, y))

  return ret

#Updates each cell with known info
def updateBoardKnowledge(board,n):
    dim=len(board)
    for row in range(0,dim):
        for col in range(0,dim):
            clue,neighbors,visibleMineCount,visibleSafeSpace=checkSurrounding(board,row, col)
            board[row][col].clue=clue
            board[row][col].minesAround=visibleMineCount
            board[row][col].safeAround=visibleSafeSpace
            board[row][col].hiddenAround=neigbors-visibleMineCount-visibleSafeSpace

def basicAgent(d, n):
  board = generateBoard(d, n)
  bombCount = 0
  while bombCount < n:
    printBoard(board)
    i = random.randint(0, len(board)-1)
    j = random.randint(0, len(board)-1)
    print(str(i) + " " + str(j))
    board[i][j].setVisible(True)
    if board[i][j].getMine():
            bombCount += 1
    for (x, y) in getNewNeighbors(board, i, j):
        board[x][y].setVisible(False)


  printBoard(board)

def main():
    #FOR TESTING
    board = generateBoard(5, 3)
    printBoard(board)
    #basicAgent(5, 3)

if __name__=="__main__":
    main()