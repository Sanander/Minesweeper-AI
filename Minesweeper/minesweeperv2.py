import random
import queue
import math
import copy
import matplotlib.pyplot as plt
import numpy

#Data structure representing each square on the grid and its associated
#information
class Square:

  def __init__(self, mine=False, clue=0, minesAround=0, safeAround=0, hiddenAround=0, visible=None):  

    self.mine = mine
    self.clue = clue
    self.minesAround = minesAround
    self.safeAround = safeAround
    self.hiddenAround = hiddenAround
    self.visible = visible

  def getMine(self):
    return self.mine

  def setMine(self, mine=True):
    self.mine = mine
    return

  def getClue(self):
    return self.clue

  def setClue(self, clue):
    self.clue = clue
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
      return str(self.clue)
    if self.getMine():
      return "M"
    return str(self.clue)

#Data structure to store a piece of info in knowledge base
class Fact:
    #Spaces=set square indexes
    def __init__(self, spaces, numberOfMines):
        self.setOfSpaces = spaces
        self.numberOfMines = numberOfMines

    def __str__(self):
        return (str(self.setOfSpaces) + ": " + str(self.numberOfMines) + "\n")

    def __repr__(self):
        return str(self)

#Creates board
def generateBoard(d, n):
  board = [[Square() for x in range(d)] for x in range(d)]
  
  x = 0
  while (n > x):
    i = random.randint(0, d - 1)
    j = random.randint(0, d - 1)
    if (board[i][j].getMine() == False):
        board[i][j].setMine(True)
        x+=1
  
  for i in range(d):
     for j in range(d):
       board[i][j].setClue(checkSurrounding(board, i, j))

  return board

#Get info on neigbors
def checkSurrounding(board, i, j):
  clue = 0
  visibleMineCount = 0
  visibleSafeSpace = 0
  neighbors = 0
  for x in range(i - 1, i + 2):
    for y in range(j - 1, j + 2):
      if (x >= 0 and y >= 0):
        if (x < len(board) and y < len(board)):
            neighbors = neighbors + 1
            if (board[x][y].getMine()):
                clue += 1
                if(board[x][y].getVisible() == True):
                    visibleMineCount+=1
            elif (board[x][y].getVisible() == True):
                    visibleSafeSpace = visibleSafeSpace + 1
  return (clue,neighbors,visibleMineCount,visibleSafeSpace)

#Display board
def printBoard(board):
  for x in range(len(board)):
     for y in range(len(board)):
       print(str(board[x][y]), end=" ")
     print("\n")
  print("\n")

#Get list of hidden neigbors
def getNewNeighbors(board, i, j):
  ret = []
  
  for x in range(i - 1, i + 2):
    for y in range(j - 1, j + 2):
      if (x != i or y != j):
        if (x >= 0 and y >= 0):
          if (x < len(board) and y < len(board)):
            if (board[x][y].getVisible() == None):
              ret.append((x, y))

  return ret

#Get list of revealed neigbors
def getRevealedNeighbors(board, i, j):
  ret = []
  
  for x in range(i - 1, i + 2):
    for y in range(j - 1, j + 2):
      if (x != i or y != j):
        if (x >= 0 and y >= 0):
          if (x < len(board) and y < len(board)):
            if ((board[x][y].getVisible() == True) and not (board[x][y].getMine())):
              ret.append((x, y))

  return ret

#Updates each cell with known info
def updateBoardKnowledge(board,n=0):
    dim = len(board)
    for row in range(0,dim):
        for col in range(0,dim):
            clue,neighbors,visibleMineCount,visibleSafeSpace = checkSurrounding(board,row,col)
            board[row][col].clue = clue
            board[row][col].minesAround = visibleMineCount
            board[row][col].safeAround = visibleSafeSpace
            board[row][col].hiddenAround = neighbors - visibleMineCount - visibleSafeSpace

#Basic agent specefied in assignment
def basicAgent(board, n=0):
  bombCount = 0
  minesFlagged = 0
  visited = []
  dim = len(board)
  boardChanged = False

  while(len(visited)<len(board)**2):
    boardChanged = False
    #printBoard(board)
    updateBoardKnowledge(board,n)
    #Search revealed squares to see if neighbors can be solved
    for (row,col) in visited:
        if (board[row][col].getMine()):
          continue
        clue = board[row][col].clue
        revealedMines = board[row][col].minesAround
        hiddenNeighbors = board[row][col].hiddenAround
        safeNeighbors = board[row][col].safeAround
        totalNeighbors = revealedMines + safeNeighbors + hiddenNeighbors
        
        #print("ROW-COL: "+str(row)+", "+str(col)+", "+str(revealedMines))

        #Case all neighbors are mines
        if(clue - revealedMines == hiddenNeighbors):
            hiddenList = getNewNeighbors(board,row,col)
            for (i,j) in hiddenList:
                if((i,j) not in visited):
                    #print("Flag mine on: "+str(i)+", "+str(j))
                    minesFlagged+=1
                    bombCount+=1
                    board[i][j].setVisible(True)
                    visited.append((i,j))
                    boardChanged = True
                    if not board[i][j].mine:
                                raise Exception("Mine Misflagged")
            
        #Case all neighbors are safe
        elif (totalNeighbors - clue - safeNeighbors == hiddenNeighbors):
            hiddenList = getNewNeighbors(board,row,col)
            for (i,j) in hiddenList:
                if ((i,j) not in visited):
                    #print("Reveal: "+str(i)+", "+str(j))
                    board[i][j].setVisible(True)
                    visited.append((i,j))
                    boardChanged = True

        if(boardChanged):
            break

    #If no conclusive decision choose random
    if not boardChanged:
        i = random.randint(0, len(board) - 1)
        j = random.randint(0, len(board) - 1)
        while((i,j) in visited):
            i = random.randint(0, len(board) - 1)
            j = random.randint(0, len(board) - 1)
        #print("Randomly Select: "+str(i)+", "+str(j))
        board[i][j].setVisible(True)
        if board[i][j].getMine():
            bombCount += 1
        visited.append((i,j))
  #print("MINES FLAGGED BASIC: "+str(minesFlagged))
  #printBoard(board)
  return minesFlagged

#Updates the knowledge base when a cell is revealed
def updateBoardKnowledgeAdv(board,row,col,knowledge):
    newSpace = board[row][col]

    #Modify Knowledge Base If Revealed Space is Safe
    if not newSpace.mine:

        #Remove newly revealed space from sets in knowledge
        for item in knowledge:
            if((row,col) in item.setOfSpaces):
                item.setOfSpaces.remove((row,col))

        #When clue is revealed add neighbors defined by that clue to knowledge
        #base
        knowledge.append(Fact(set(getNewNeighbors(board,row,col)),newSpace.clue - newSpace.minesAround))

    else:
        #Remove newly revealed space from sets in knowledge and decrease mine
        #count
        for item in knowledge:
            if((row,col) in item.setOfSpaces):
                item.setOfSpaces.remove((row,col))
                item.numberOfMines-=1
    return knowledge

#Remove duplicates and empty sets from list
def removeDuplicates(knowledge):
    if len(knowledge) >= 0 and knowledge[0].setOfSpaces == set():
        #print("DEL Empty: "+ str(knowledge[0]))
        del knowledge[0]

    for i in range(0,len(knowledge) - 1):
        j = i + 1
        while j < len(knowledge):
            item1 = knowledge[i]
            item2 = knowledge[j]
            if (item2.setOfSpaces) == set():
                #print("DEL Empty: "+ str(knowledge[j]))
                del knowledge[j]
                j = j - 1
            if (item1.setOfSpaces.difference(item2.setOfSpaces)) == set() and (item2.setOfSpaces.difference(item1.setOfSpaces))==set():
                #print("DEL Duplicate: "+ str(item1.setOfSpaces)+" ... "+str(item2.setOfSpaces))
                del knowledge[j]
                j = j - 1
            j+=1

    return knowledge

#Updates the information about each square and its neighbors
def createNewKnowledge(board, knowledge):
    removeDuplicates(knowledge)

    newInfo = []

    for i in range(0,len(knowledge) - 1):
        for j in range(i + 1,len(knowledge)):

            item1 = knowledge[i]
            item2 = knowledge[j]

            if (item1.setOfSpaces.issubset(item2.setOfSpaces)):
                newFact = Fact(item2.setOfSpaces.difference(item1.setOfSpaces),item2.numberOfMines - item1.numberOfMines)
                if newFact not in knowledge and newFact not in newInfo:
                    newInfo.append(newFact)
                    #print(str(item1)+" is a subset of "+ str(item2))
            elif (item2.setOfSpaces.issubset(item1.setOfSpaces)):
                newFact = Fact(item1.setOfSpaces.difference(item2.setOfSpaces),item1.numberOfMines - item2.numberOfMines)
                if newFact not in knowledge and newFact not in newInfo:
                    newInfo.append(newFact)
                    #print(str(item2)+" is a subset of "+ str(item1))
    knowledge.extend(newInfo)

#Probability based selection if no definitive squares can be revealed
def improvedSelection(board,visited,n,mineCount):
    #If no conclusive decision choose lowest probability of mine
        prob = 1
        i = random.randint(0, len(board) - 1)
        j = random.randint(0, len(board) - 1)
        isRandom = True
        
        #Attempt to find a neighboring space with a low probability of being a
        #mine
        for (x, y) in visited:
          if (board[x][y].hiddenAround > 0 and not board[x][y].mine):
            if ((board[x][y].clue - board[x][y].minesAround) / board[x][y].hiddenAround < prob):
              (i, j) = getNewNeighbors(board, x, y)[0]
              prob = (board[x][y].clue - board[x][y].minesAround) / board[x][y].hiddenAround
              isRandom = False
              print("random neighbor "+str(prob))

        #If a random space is less likely to be a mine then choose the random
        #space
        val=(n-mineCount) / (len(board) ** 2 - len(visited))
        print((val))
        if(val < prob):
            isRandom = True
            while ((i,j) in visited):
                i = random.randint(0, len(board) - 1)
                j = random.randint(0, len(board) - 1)
            print("Dont do neigbor")
               
        #Chooses random space if there are no revealed spaces
        while ((i,j) in visited):
                i = random.randint(0, len(board) - 1)
                j = random.randint(0, len(board) - 1)

        #if (isRandom):
        #  print("Randomly Select: "+str(i)+", "+str(j))
        #else:
        #  print("Probability Select: "+str(i)+", "+str(j))

        return (i,j)

#Advanced agent with knowledge base and improved selection method
def advancedAgent(board, n=0,globalToggle=False):
  bombCount = 0
  minesFlagged = 0
  visited = []
  knowledge = []
  dim = len(board)
  boardChanged = False

  if globalToggle:
      updateBoardKnowledge(board,n)
      globalSet=set()
      for row in range(0,len(board)):
          for col in range(0,len(board)):
              globalSet.add((row,col))
      knowledge.append(Fact(globalSet,n))


  while (len(visited)<len(board)**2):
    #print("\n")
    #print("_____________________________________________________________")
    #print("State at beginning of turn")
    #print(str(knowledge))
    #printBoard(board)

    boardChanged = False


    newSpaces = []

    #print("Decision Made:")
    if len(knowledge) > 0:

        createNewKnowledge(board,knowledge)

        for item in knowledge:
            newSpaces = []

            removeItem = False

            setOfSpaces = item.setOfSpaces
            numberOfMines = item.numberOfMines

            #If set length in knowledge equals number of mines, all mines
            if len(setOfSpaces) == numberOfMines:
                removeItem = True
                for (i,j) in setOfSpaces:
                        if((i,j) not in visited):
                            #print("Flag mine on: " + str(i) + ", " + str(j))
                            minesFlagged+=1
                            bombCount+=1
                            board[i][j].setVisible(True)
                            visited.append((i,j))
                            boardChanged = True
                            updateBoardKnowledge(board)
                            updateBoardKnowledgeAdv(board,i,j,knowledge)
                            if not board[i][j].mine:
                                raise Exception("Mine Misflagged")
                            break

            #If knowledge mine count=0, all safe
            elif numberOfMines == 0 and not boardChanged:
                removeItem = True
                for (i,j) in setOfSpaces:
                        if((i,j) not in visited):
                            #print("Revealed: "+str(i)+", "+str(j))
                            board[i][j].setVisible(True)
                            visited.append((i,j))
                            boardChanged = True
                            updateBoardKnowledge(board)
                            updateBoardKnowledgeAdv(board,i,j,knowledge)
                            break

            if boardChanged:
                break
                
                
#If no conclusive decision choose random

    #IMPROVED SEARCH
    #if not boardChanged:
    #    (i,j) = improvedSelection(board,visited,n,bombCount)
    #    #print("Randomly Select: "+str(i)+", "+str(j))
    #    board[i][j].setVisible(True)
    #    if board[i][j].getMine():
    #        bombCount += 1
    #    visited.append((i,j))
    #    updateBoardKnowledge(board,n)
    #    updateBoardKnowledgeAdv(board,i,j,knowledge)

    #RANDOM SEARCH
    if not boardChanged:
        i = random.randint(0, len(board) - 1)
        j = random.randint(0, len(board) - 1)
        while((i,j) in visited):
            i = random.randint(0, len(board) - 1)
            j = random.randint(0, len(board) - 1)
        #print("Randomly Select: "+str(i)+", "+str(j))
        board[i][j].setVisible(True)
        if board[i][j].getMine():
            bombCount += 1
        visited.append((i,j))
        updateBoardKnowledge(board)
        updateBoardKnowledgeAdv(board,i,j,knowledge)
    
  #printBoard(board)
  #print("MINES FLAGGED: "+str(minesFlagged))
  return minesFlagged

def main():
    ##FOR TESTING
    #dim = 5
    #n = 3
    #x2 = 0
    
    #board = generateBoard(dim, n)
    ##board2=copy.deepcopy(board)
    ##x1=(basicAgent(board2,n))
    #x2 = advancedAgent(board, n, True)
    ##print(x1)
    #print(x2)

#Advanced Agent Play-by-Play
    dim = 10
    n = 5
    x2 = 0
    
    board = generateBoard(dim, n)
    x2 = basicAgent(board)
    print("Mines Flagged: "+str(x2)+" out of "+str(n))

#Performance Graphs
    #dim=5
    #dataPoints=4
    #numberOfTrials=5
    #nVals=[5,10,15,20]
   
    #scoreBasic=[0]*dataPoints
    #scoreAdv=[0]*dataPoints
    #print(nVals)
    #for i in range(0,dataPoints):
    #    print(i)
    #    for j in range(0,numberOfTrials):
    #        print(j)
    #        board = generateBoard(dim, nVals[i])
    #        board2=copy.deepcopy(board)
    #        scoreBasic[i]+=basicAgent(board,nVals[i])
    #        scoreAdv[i]+=advancedAgent(board2,nVals[i],False)
    #    scoreBasic[i]=scoreBasic[i]/(nVals[i]*numberOfTrials)
    #    scoreAdv[i]=scoreAdv[i]/(nVals[i]*numberOfTrials)
  
    #print(scoreBasic)
    #print(scoreAdv)

    #plt.scatter(nVals,scoreBasic,color='b',label="Basic Agent")
    #plt.scatter(nVals,scoreAdv, color='r', label="Advanced Agent")
    #plt.xlabel("Number of Mines")
    #plt.ylabel("Avg Fraction of Mines Flagged")
    #plt.title("Fraction Flagged vs Number of Mines "+str(dim)+"x"+str(dim)+"board")
    #plt.legend(loc="upper right")
    #plt.show()

if __name__ == "__main__":
    main()