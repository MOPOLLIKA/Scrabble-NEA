import pygame
import os
import random
import time
import json
import wordCheckAPI as wc
from typing import Iterable, Literal
from numpy import transpose
#from wordCheck import isWord
from dawg import Trie, listToStr
from copy import deepcopy

WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
RED: tuple = (255, 0, 0)
ORANGEDARK: tuple = (139, 64, 0)
AMARANTH: tuple = (159, 43, 104)
GREENPOOL: tuple = (10, 108, 3)
BROWNDARK: tuple = (92, 64, 51)
BROWNLIGHT: tuple = (196, 164, 132)

# 1470:956 - the real resolution, 1280:800 - the chosen resolution
WIDTH = 1470
HEIGHT = 829

LETTERS_SCORES: dict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, 
            "O": 1, "P": 3,"Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "BLANK": 0}

trie = Trie()

with open("MyDictionary.json", "r") as f:
    words = json.load(f)
    f.close()

trie = Trie()
trie.assemble(words)
def isWord(word: str) -> bool:
    return trie.bashSearch(word)

class Highlighters:
    BRIGHTBLUE: str = "\033[94m"
    BRIGHTMAGENTA: str = "\033[95m"
    BRIGHTGREEN: str = "\033[92m"
    BRIGHTRED: str = "\033[91m"
    BRIGHTYELLOW: str = "\033[93m"
    ENDC: str = "\033[0m"
    BOLD: str = "\033[1m"
    UNDERLINE: str = '\033[4m'
    ITALIC: str = '\033[3m'

def highlight(text: str, highlighting: Highlighters) -> str:
    return highlighting + text + Highlighters.ENDC

def indicateTile(tileType: str) -> str:
    highlighting: str = ""
    match tileType:
        case "DL":
            highlighting = Highlighters.BRIGHTBLUE
        case "TL":
            highlighting = Highlighters.BRIGHTMAGENTA
        case "DW":
            highlighting = Highlighters.BRIGHTGREEN
        case "TW":
            highlighting = Highlighters.BRIGHTRED
        case "ST":
            highlighting = Highlighters.BRIGHTYELLOW
        case _:
            highlighting = ""
    return highlight(tileType, highlighting)

def letterMultiplicator(tileType: str) -> int:
    match tileType:
        case "DL":
            return 2
        case "TL":
            return 3
        case _:
            return 1

def wordMultiplicator(tileType: str) -> int:
    match tileType:
        case "DW":
            return 2
        case "TW":
            return 3
        case "ST":
            return 2
        case _:
            return 1

def lettersTransform(dct: dict) -> list:
    result: list = []
    for letter, numberOfLetters in dct.items():
        result += [letter for _ in range(numberOfLetters)]
    return result


class LetterBag:
    def __init__(self) -> None:
        self.bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6,
                "O": 8, "P": 2,"Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}

    def __repr__(self) -> str:
        return f"Letters left: {self.bag}"
    
    def refresh(self) -> None:
        self.bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2,"N": 6, 
                "O": 8, "P": 2,"Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}
    
    def isEmpty(self) -> bool:
        for value in self.bag.values():
            if value != 0:
                return False
        return True
    
    def numberOfLettersRemaining(self) -> int:
        return sum(self.bag.values())
    
    def getLetter(self) -> str:
        if not self.isEmpty():
            lettersTransformed: list = lettersTransform(self.bag)
            index = random.randint(0, len(lettersTransformed) - 1)
            letter: str = lettersTransformed.pop(index)
            self.bag[letter] -= 1
            return letter
        else:
            return "No letters left in the letter bag"
        
    def returnLetter(self, letter: str) -> None:
        self.bag[letter] += 1

# LR - letter, DL - double letter, TL - triple letter,  DW - double word, TW - triple word, ST - start point
class Board:
    def __init__(self) -> None:
        self.board: list[list[str]] = [[" " for _ in range(15)] for _ in range(15)]
        self.boardTypes: list[list[str]] = [["LR" for _ in range(15)] for _ in range(15)]
        self.bag: LetterBag = LetterBag()
        self.isFirstTurn: bool = True
        # initialise tile types
        for row in range(15):
            for col in range(15):
                if (col in {0, 7, 14} and row in {0, 7, 14}) and not (col == 7 and row == 7):
                    self.boardTypes[row][col] = "TW"
                elif (col in {3, 11} and row in {0, 7, 14}) or (col in {0, 7, 14} and row in {3, 11}) or\
                (col in {6, 8} and row in {2, 6, 8, 12}) or (col in {2, 12} and row in {6, 8}):
                    self.boardTypes[row][col] = "DL"
                elif (col in {1, 13} and row in {1, 13}) or (col in {2, 12} and row in {2, 12}) or\
                (col in {3, 11} and row in {3, 11}) or (col in {4, 10} and row in {4, 10}):
                    self.boardTypes[row][col] = "DW"
                elif (col in {5, 9} and row in {1, 5, 9, 14}) or (col in {1, 13} and row in {5, 9}):
                    self.boardTypes[row][col] = "TL"
        self.boardTypes[7][7] = "ST"
    
    
    def __repr__(self) -> str | None:
        for rowElements in self.board:
            print("|", end="")
            print("-" * 59, end="")
            print("|")
            for colElement in rowElements:
                print("| ", end="")
                print(colElement, end=" ")
            print("|")
        print("|", end="")
        print("-" * 59, end="")
        print("|", end="")
        print()
        return ""
    
    def printTypes(self) -> None:
        for rowElements in self.boardTypes:
            print("|", end="")
            print("-" * 74, end="")
            print("|")
            for colElement in rowElements:
                print("| ", end="")
                indicatedTile = indicateTile(colElement)
                print(indicatedTile, end=" ")
            print("|")
        print("|", end="")
        print("-" * 74, end="")
        print("|", end="")
        print()
    
    def placeLetter(self, col: int, row: int, letter: str) -> None:
        if self.board[row][col] != " ":
            return 
        self.board[row][col] = letter

    def removeLetter(self, col: int, row: int) -> None:
        self.board[row][col] = " "
        
    def searchForWords(self) -> list:
        wordsFound: list = []
        for rowElements in self.board: 
            wordsFound += findWordsInRow(rowElements)[0]
        for colElements in transpose(self.board):
            colElements = list(colElements)
            wordsFound += findWordsInRow(colElements)[0]
        return wordsFound
    
    def isValid(self) -> bool:
        # Checks whether the board is valid in terms of validity of words
        valid = isBoardValid(self.board)
        # checks whether a letter is placed on the starting tile at the start of the game
        if self.isFirstTurn:
            if self.board[7][7] == " ":
                return False
        return valid
    
    def fitWord(self, word: str) -> list[tuple]:
        """Searches the board for where to put the word inputted. It returns a list of triples (col, row, letter)
        identifying where to put letters.
        If there is nowhere to place the word, it returns an empty list."""
        for row in range(15):
            for col in range(15):
                boardLetter = self.board[row][col]
                if boardLetter not in word:
                    continue

                # Searching for a word horizontally
                left: list = scanLeft(col, row, self.board)
                right: list = scanRight(col, row, self.board)
                horizontalWord: str = listToStr(left) + boardLetter + listToStr(right)

                # Searching for a word vertically
                up: list = scanUp(col, row, self.board)
                down: list = scanDown(col, row, self.board)
                verticalWord: str = listToStr(up) + boardLetter + listToStr(down)

                # Determining the X and Y steps
                horizontal = isWord(horizontalWord)
                vertical = isWord(verticalWord)
                stepX = 0
                stepY = 0
                # If the horizontal is used, go vertically
                if horizontal and not vertical:
                    stepY = 1
                # If the vertical is used, go horizontally
                elif not horizontal and vertical:
                    stepX = 1
                # If the letter is the intersection of a vertical and a horizontal words, then skip
                elif horizontal and vertical:
                    continue

                letterIndices = [index for index in range(len(word)) if word[index] == boardLetter]
                for letterIndex in letterIndices:
                    boardCopy = deepcopy(self.board)
                    moves = []
                    
                    # set up the starting column and row to place the proposed word
                    currentCol = col - letterIndex * stepX
                    currentRow = row - letterIndex * stepY

                    for letter in word:
                        boardCopy[currentRow][currentCol] = letter
                        moves.append((currentCol, currentRow, letter))
                        currentCol += stepX
                        currentRow += stepY

                    if isBoardValid(boardCopy):
                        return moves
        return []

    def getBoardElements(self) -> list[list[str]]:
        return self.board
    
    def getBoardTypes(self) -> list[list[str]]:
        return self.boardTypes
    
def isBoardValid(board: list[list[str]]) -> bool:
    for row in range(15):
        for col in range(15):
            letter: str = board[row][col]
            if letter == " ":
                continue
            
            # searching for a word horizontally
            left: list = scanLeft(col, row, board)
            right: list = scanRight(col, row, board)
            horizontalWord: str = listToStr(left) + letter + listToStr(right)
            if len(horizontalWord) != 1 and not isWord(horizontalWord):
                return False
            
            # searching for a word vertically
            up: list = scanUp(col, row, board)
            down: list = scanDown(col, row, board)
            verticalWord: str = listToStr(up) + letter + listToStr(down)
            if len(verticalWord) != 1 and not isWord(verticalWord):
                return False
            
            # check if it is a single standalone letter, pertaining to no word on the board
            if len(horizontalWord) == 1 and len(verticalWord) == 1:
                return False
    return True


def scanLeft(col: int, row: int, board: list[list[str]]) -> list:
    result: list = []
    step: int = -1
    letterCurrent: str = ""
    while letterCurrent != " ":
        result.append(letterCurrent)
        col = col + step
        row = row
        if not (0 <= col <= 14) or not (0 <= row <= 14):
            break
        letterCurrent = board[row][col]
    result.remove("")
    result.reverse()
    return result
    
def scanRight(col: int, row: int, board: list[list[str]]) -> list:
    result: list = []
    step: int = 1
    letterCurrent: str = ""
    while letterCurrent != " ":
        result.append(letterCurrent)
        col = col + step
        row = row
        if not (0 <= col <= 14) or not (0 <= row <= 14):
            break
        letterCurrent = board[row][col]
    result.remove("")
    return result
    
def scanUp(col: int, row: int, board: list[list[str]]) -> list:
    return scanLeft(row, col, transpose(board))
    
def scanDown(col: int, row: int, board: list[list[str]]) -> list:
    return scanRight(row, col, transpose(board))

def findWordsInRow(rowElements) -> tuple[list, bool]:
    row: str = "".join(rowElements)
    words: list = [element for element in row.split(" ") if element != ""]
    isCorrect: bool = True if False not in map(lambda x: isWord(x), words) else False
    words = [word for word in words if isWord(word)]
    return words, isCorrect
                    

class Player:
    ID = 1

    def __init__(self) -> None:
        self.letters: list[str] = []
        self.score: int = 0
        self._temporaryScore: int = 0
        self.id: int = Player.ID
        self.name: str = f"Player {self.id}" # implement name selection later in the settings TODO
        self.active: bool = False
        self.placingLetter: bool = False
        self.bot: bool = False
        Player.ID += 1

    def __repr__(self) -> str:
        return f"Player {self.id}, Name: {self.name}, Score: {self.score}, Letters: {self.letters}, isActive: {self.active}\n"
    
    def takeLetters(self, letterBag: LetterBag) -> None | bool:
        for _ in range(7 - len(self.letters)):
            letter = letterBag.getLetter()
            if letter:
                self.letters.append(letter)
            else:
                return False, "The letter bag is empty!"
    
    def addLetter(self, letter: str) -> None:
        if len(self.letters) == 7:
            return
        self.letters.append(letter)

    def removeLetter(self, letter: str) -> None:
        if not letter == " ":
            self.letters.remove(letter)
        
    def placeLetter(self, letter: str, col: int, row: int, board: Board) -> None:
        if not self.letters:
            return
        self.letters.remove(letter)
        board.placeLetter(col, row, letter)
    
    def applyMoves(self, board: Board, moves: list[tuple]) -> None:
        for col, row, letter in moves:
            self.placeLetter(letter, col, row, board)
        
    def adjustScore(self, adjustment: int) -> None:
        self.score += adjustment

    def setTemporaryScore(self, score: int) -> None:
        self._temporaryScore = score

    def switchActive(self) -> None:
        self.active = not self.active

    def switchLetterPlacement(self) -> None:
        self.placingLetter = not self.placingLetter

    def switchBot(self) -> None:
        self.bot = not self.bot

    def isActive(self) -> bool:
        return self.active
    
    def isBot(self) -> bool:
        return self.bot
    
    def isPlacingLetter(self) -> bool:
        return self.placingLetter
    
    def getTemporaryScore(self) -> int:
        return self._temporaryScore
    
    def getNumberOfTiles(self) -> int:
        return len(self.letters)
    
    def getLetters(self) -> list[str]:
        return self.letters
    
    def getId(self) -> int:
        return self.id
    
    def getName(self) -> str:
        return self.name
    
    def getScore(self) -> int:
        return self.score
    

class Simulation:
    def __init__(self) -> None:
        self.board: Board = Board()
        self.numberOfPlayers: int
        self.players: list[Player]

    def startGame(self) -> None:
        print()
        print(highlight("You are playing bumble Scrabble!", Highlighters.BOLD))
        print()
        self.numberOfPlayers = int(input("Please, select 2, 3 or 4 players: "))
        self.players = [Player() for _ in range(self.numberOfPlayers)]

        enter = input("Press enter to see your letters: ")
        while enter:
            enter = input()

        for player in self.players:
            player

class PlayerQueue:
    def __init__(self, players: Iterable[Player]):
        self.queue: list[Player] = [player for player in players]
        self.originalElements: list[Player] = self.queue.copy()
        self.length: int = len(self.queue)

    def __repr__(self) -> str:
        print(self.queue)
        return ""
    
    def rotate(self) -> Player:
        playerPrevious: Player = self.queue[-1]
        playerPrevious.switchActive()
        playerNext: Player = self.queue.pop(0)
        playerNext.switchActive()
        self.queue.insert(self.length, playerNext)
        return playerNext
    
    def getOriginalElements(self) -> list[Player]:
        return self.originalElements
    
    def getLength(self) -> int:
        return self.length


class Turn:
    def __init__(self):
        self.turn: list[tuple] = [] # [(col1, row1), (col2, row2), ..., (coln, rown)]

    def initialiseFromMoves(self, moves: list[tuple]):
        for col, row, _ in moves:
            self.turn.append((col, row))

    def add(self, coords: tuple["col": int, "row": int]) -> None:
        self.turn.append(coords)

    def remove(self, coords: tuple["col": int, "row": int]) -> None:
        self.turn.remove(coords)

    def refresh(self) -> None:
        self.turn = []

    def isValid(self) -> bool:
        if not self.turn:
            return False
        if len(self.turn) == 1:
            return True
        
        cols: list[int] = [col for col, _ in self.turn]
        uniqueCols: list[int] = set(cols)
        rows: list[int] = [row for _, row in self.turn]
        uniqueRows: list[int] = set(rows)
        if (len(uniqueCols) == 1 and len(uniqueRows) >= 1) or (len(uniqueCols) >= 1 and len(uniqueRows) == 1):
            return True
        else:
            return False

    # calling this method only occurs after checking turn.isValid() and board.isValid()
    def calculateScore(self, board: Board) -> int:
        """
        To calculate score, every move(tile placed) is inspected to find if there are any connected words to it horizontally
        and then vertically. When it finds such a connection, it goes through the word and inspects each tile on the matter 
        of whether it was placed during the turn(that allows multiplicators that could be activating the letter
        work properly - multiplicators don't work twice) and what score does this letter represent. Then the score of each 
        letter is multiplied by letterMultiplicator of the board cell, the results added and multiplied by wordMultiplicator.
        Also, the multiplicators should work for all simultaneous words in 
        """
        score: int = 0
        usedHorizontalWords: dict[str, list[tuple]] = {} # {"ADD": [(colA, rowA), (colD, rowD), (colD, rowD)], ...}
        usedVerticalWords: dict[str, list[tuple]] = {} 
        boardElements = board.getBoardElements()
        boardTypes = board.getBoardTypes()

        for col, row in self.turn:
            letter: str = boardElements[row][col]

            # searching for a word horizontally
            left: list = scanLeft(col, row, boardElements)
            right: list = scanRight(col, row, boardElements)
            horizontalWord: str = listToStr(left) + letter + listToStr(right)

            if (not isWord(horizontalWord)) or (horizontalWord in usedHorizontalWords):
                continue

            # going through the horizontal word found connected to the (col, row) tile
            usedHorizontalWords[horizontalWord] = []
            colWord: int = col - len(left)
            rowWord: int = row
            horizontalScore: int = 0
            wordMult: int = 1
            tileType: str
            for wordLetter in horizontalWord:
                if (colWord, rowWord) in self.turn:
                    # if the tile is in the turn, then apply all the multiplicators
                    tileType = boardTypes[rowWord][colWord]
                else:
                    # else it is a standard letter with no multiplicator, even if the tile contained some multiplicator
                    tileType = "LR"

                wordMult *= wordMultiplicator(tileType)
                letterMult = letterMultiplicator(tileType)
                usedHorizontalWords[horizontalWord].append((colWord, rowWord))
                letterScore: int = LETTERS_SCORES[wordLetter]
                horizontalScore += letterScore * letterMult

                colWord = colWord + 1
                rowWord = rowWord
            horizontalScore *= wordMult
            score += horizontalScore

        for col, row in self.turn:
            letter: str = boardElements[row][col]

             # searching for a word vertically
            up: list = scanUp(col, row, boardElements)
            down: list = scanDown(col, row, boardElements)
            verticalWord: str = listToStr(up) + letter + listToStr(down)

            if (not isWord(verticalWord)) or (verticalWord in usedVerticalWords):
                continue

            # going through the vertical word found connected to the (col, row) tile
            usedVerticalWords[verticalWord] = []
            colWord: int = col
            rowWord: int = row - len(up)
            verticalScore: int = 0
            wordMult: int = 1
            tileType: str
            for wordLetter in verticalWord:
                if (colWord, rowWord) in self.turn:
                    # if the tile is in the turn, then apply all the multiplicators
                    tileType = boardTypes[rowWord][colWord]
                else:
                    # else it is a standard letter with no multiplicator, even if the tile contained some multiplicator
                    tileType = "LR"

                wordMult *= wordMultiplicator(tileType)
                letterMult = letterMultiplicator(tileType)
                usedVerticalWords[verticalWord].append((colWord, rowWord))
                letterScore: int = LETTERS_SCORES[wordLetter]
                verticalScore += letterScore * letterMult

                colWord = colWord
                rowWord = rowWord + 1
            verticalScore *= wordMult
            score += verticalScore

        return score
    
    def getTurn(self) -> list[tuple]:
        return self.turn


class Bot(Player):
    def __init__(self):
        super().__init__()
        self.bot = True
        self.difficulty = 6

    def makeTurn(self, board: Board) -> int:
        """Heuristic method which finds the best turn a player can make, given his 
        letters and a board configuraiton.
        It applies the turn to the board, calculates the score and adds the score to the bot player.
        Returns True if an optimal turn was found, otherwise returns False and the turn is skipped."""
        optimalWords = trie.generateOptimalWord(letters=self.getLetters(), difficulty=self.difficulty)
        for optimalWord in optimalWords:
            moves = board.fitWord(optimalWord)
            # If not possible to place a word, continue to the next possible word
            if moves == []:
                continue
            self.applyMoves(board, moves)
            turn = Turn()
            turn.initialiseFromMoves(moves)
            score = turn.calculateScore(board)
            self.adjustScore(score)
            return True
        return False

def drawBoard(board: Board) -> None:
    sideLength: float = 0.7 * HEIGHT
    gridLength: float = sideLength / 15

    startXPos: float = 0.5 * WIDTH - 0.5 * sideLength
    endXPos: float = 0.5 * WIDTH + 0.5 * sideLength
    startYPos: float = 0.15 * HEIGHT
    endYPos: float = 0.85 * HEIGHT

    pygame.draw.rect(screen, BROWNDARK, [startXPos, startYPos, sideLength, sideLength])

    # drawing grid
    for i in range(15 + 1):
        pygame.draw.line(screen, BLACK, (startXPos, startYPos + i * gridLength), (endXPos, startYPos + i * gridLength), 3) # horizontal
        pygame.draw.line(screen, BLACK, (startXPos + i * gridLength, startYPos), (startXPos + i * gridLength, endYPos), 3) # vertical 
    

    tileStartXPos: float = startXPos + (gridLength / 2)
    tileStartYPos: float = startYPos + (gridLength / 2)

    # drawing type tiles on the board
    types: list[list[str]] = board.getBoardTypes()
    for row in range(15):
        for col in range(15):
            xTile: float = tileStartXPos + (col * gridLength)
            yTile: float = tileStartYPos + (row * gridLength)
            
            typeTile: str = types[row][col]
            if typeTile == "LR":
                continue
            typeTileFilename: str = os.path.join("TypeTileImagesBoard", typeTile + ".png")
            drawTile((xTile, yTile), typeTileFilename)

    # drawing letter tiles on the board
    tiles: list[list[str]] = board.getBoardElements()
    for row in range(15):
        for col in range(15):
            xTile: float = tileStartXPos + (col * gridLength)
            yTile: float = tileStartYPos + (row * gridLength)
            
            letter = tiles[row][col]
            if letter == " ":
                continue
            key: int = (row + 1) * (col + 1)
            tileFilenameRaw: str = letterToTileFilename(letter, key, isBoardSize=True)
            tileFilename: str = os.path.join("TileImagesBoard", tileFilenameRaw)
            drawTile((xTile, yTile), tileFilename)

    # drawing grid annotation numbers
    for row in range(15):
        numberAnnotation: str = str(row + 1)
        xNumberLeft: float = tileStartXPos - gridLength
        xNumberRight: float = tileStartXPos + 15 * gridLength
        yTile: float = tileStartYPos + (row * gridLength)
        drawText((xNumberLeft, yTile), numberAnnotation, "small")
        drawText((xNumberRight, yTile), numberAnnotation, "small")

    # drawing grid annotation letters
    for col in range(15):
        letterAnnotation: str = chr(ord("A") + col)
        xTile: float = tileStartXPos + (col * gridLength)
        yLetterUp: float = tileStartYPos - gridLength
        yLetterDown: float = tileStartYPos + 15 * gridLength
        drawText((xTile, yLetterUp), letterAnnotation, "small")
        drawText((xTile, yLetterDown), letterAnnotation, "small")

def drawRacks(playerQueue: PlayerQueue) -> None:
    """Variable `names` is in the following format: {'name1': numberOfTiles1, 'name2': numberOfTiles2, ...}"""
    count: int = playerQueue.getLength()
    players: list[Player] = playerQueue.getOriginalElements()
    for j in range(2):
        for i in range(2):
            if count == 0:
                break

            xPos, yPos = rackPosition(i, j)
            index: int = 2 * j + i
            player: Player = players[index]
            temporaryScore = player.getTemporaryScore()

            drawRack(xPos, yPos, player, temporaryScore)

            count -= 1

def rackPosition(i: int, j: int) -> tuple[float, float]:
    rackLength: float = 0.2 * WIDTH
    rackHeight: float = rackLength / 7 + 10
    if i == 0:
        xPos: float = (0.5 * WIDTH - 0.35 * HEIGHT) / 2 - 0.1 * WIDTH
    else:
        xPos: float = (0.5 * WIDTH + 0.35 * HEIGHT) + (0.5 * WIDTH - 0.35 * HEIGHT) / 2 - 0.1 * WIDTH

    if j == 0:
        yPos: float = 0.2 * HEIGHT
    else:
        yPos: float = 0.8 * HEIGHT - rackHeight

    return xPos, yPos

def rackPointingAt(x: int, y: int) -> Literal[0, 1, 2, 3, 4]:
    rackLength: float = 0.2 * WIDTH + 24
    rackHeight: float = rackLength / 7 + 10
    xLeft: float = (0.5 * WIDTH - 0.35 * HEIGHT) / 2 - 0.1 * WIDTH
    xRight: float = (0.5 * WIDTH + 0.35 * HEIGHT) + (0.5 * WIDTH - 0.35 * HEIGHT) / 2 - 0.1 * WIDTH
    yUp: float = 0.2 * HEIGHT
    yDown: float = 0.8 * HEIGHT - rackHeight
    
    if xLeft <= x <= xLeft + rackLength and yUp <= y <= yUp + rackHeight:
        return 1
    
    elif xRight <= x <= xRight + rackLength and yUp <= y <= yUp + rackHeight:
        return 2
    
    elif xLeft <= x <= xLeft + rackLength and yDown <= y <= yDown + rackHeight:
        return 3
    
    elif xRight <= x <= xRight + rackLength and yDown <= y <= yDown + rackHeight:
        return 4
    
    return 0

def tilePointingAtRack(x: int, xRack: int) -> Literal[0, 1, 2, 3, 4, 5, 6]:
    relativeX: int = x - xRack
    tileSide = (0.2 * WIDTH + 24) / 7
    index: int = int(relativeX / tileSide)
    return index

def drawRack(xPos: float, yPos: float, player: Player, temporaryScore: int) -> None:
    letters: list[str] = player.getLetters()
    name: str = player.getName()
    numberOfTiles: int = player.getNumberOfTiles()

    rackLength: float = 0.2 * WIDTH + 24
    rackHeight: float = rackLength / 7 + 10
    tileSide: float = rackLength / 7

    # Rack surface
    pygame.draw.rect(screen, BROWNDARK, [xPos, yPos, rackLength, rackHeight])
    for i in range(7 + 1):
        # Vertical rack borders
        pygame.draw.line(screen, BLACK, (xPos + i * tileSide, yPos), (xPos + i * tileSide, yPos + rackHeight - 1.5), width=3)
    # Top horizontal border
    pygame.draw.line(screen, BLACK, (xPos - 1, yPos), (xPos + rackLength + 1.5, yPos), width=5)
    # Bottom horizontal border
    pygame.draw.line(screen, BLACK, (xPos - 1, yPos + rackHeight - 2.5), (xPos + rackLength + 1.5, yPos + rackHeight - 2.5), width=5)
    
    nameText: pygame.Surface = mediumText.render(name, True, WHITE)
    nameTextRect = nameText.get_rect()
    nameTextRect.center = (xPos + rackLength / 2, yPos - 30)
    screen.blit(nameText, nameTextRect)

    text: str
    if temporaryScore == 0:
        text = f"Score: {player.getScore()}"
    else:
        text = f"Score: {player.getScore()} + {temporaryScore}"
    scoreText: pygame.Surface = mediumText.render(text, True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (xPos + rackLength / 2, yPos + rackHeight + 30)
    screen.blit(scoreText, scoreTextRect)

    xTileStart: float = xPos + tileSide / 2 + 3
    yTileStart: float = yPos + tileSide / 2 + 5
    for tileIndex in range(numberOfTiles):
        """
        tileImage: pygame.Surface = pygame.image.load(blankTileFilename)
        if tileImage.get_width() != tileImage.get_height() or tileImage.get_width() != tileSide:
            tileImage = pygame.transform.scale(tileImage, (tileSide, tileSide))
            filenameNew = filenameResized(blankTileFilename)
            pygame.image.save(tileImage, filenameNew)
        tileImageRect: pygame.Rect = tileImage.get_rect()
        """
        xTile: float = xTileStart + tileIndex * tileSide - 3
        isActive: bool = player.isActive()

        tileFilename: str
        if isActive:
            letter: str = letters[tileIndex]
            key: int = player.getId() ** 3
            tileFilename = letterToTileFilename(letter, key, isBoardSize=False)
            tileFilename = os.path.join("TileImagesRack", tileFilename)
        else:
            tileFilename = "TileImagesRack/Blank1.png"

        drawTile((xTile, yTileStart), tileFilename)

def drawFinishTurnButton() -> None:
    length = (0.2*WIDTH + 24)/2
    height = 0.1 * HEIGHT
    top = 0.5*HEIGHT - height/2
    left = (0.5*WIDTH + 0.35*HEIGHT) + (0.5*WIDTH - 0.35*HEIGHT)/2 - 0.1*WIDTH + (0.2*WIDTH + 24)/2

    buttonRect = pygame.rect.Rect(left, top, length, height)
    pygame.draw.rect(screen, AMARANTH, buttonRect)

    text = mediumText.render("Finish turn", True, WHITE)
    textRect = text.get_rect()
    textRect.center = buttonRect.center
    screen.blit(text, textRect)

def drawExchangeTilesButton(isHighlighted: bool) -> None:
    length = (0.2*WIDTH + 24)/2
    height = 0.1 * HEIGHT
    top = 0.5*HEIGHT - height/2
    left = (0.5*WIDTH + 0.35*HEIGHT) + (0.5*WIDTH - 0.35*HEIGHT)/2 - 0.1*WIDTH

    buttonRect = pygame.rect.Rect(left, top, length, height)
    pygame.draw.rect(screen, ORANGEDARK, buttonRect)

    text = mediumText.render("Exchange", True, WHITE)
    textRect = text.get_rect()
    textRect.center = buttonRect.center
    screen.blit(text, textRect)
    if isHighlighted:
        pygame.draw.rect(screen, RED, buttonRect, width=3)

def isPointingAtFinishButton(x: int, y: int) -> bool:
    length = (0.2*WIDTH + 24)/2
    height = 0.1 * HEIGHT
    top = 0.5*HEIGHT - height/2
    left = (0.5*WIDTH + 0.35*HEIGHT) + (0.5*WIDTH - 0.35*HEIGHT)/2 - 0.1*WIDTH + (0.2*WIDTH + 24)/2

    if left < x < left + length and top < y < top + height:
        return True
    else:
        return False

def isPointingAtExchangeButton(x: int, y: int) -> bool:
    length = (0.2*WIDTH + 24)/2
    height = 0.1 * HEIGHT
    top = 0.5*HEIGHT - height/2
    left = (0.5*WIDTH + 0.35*HEIGHT) + (0.5*WIDTH - 0.35*HEIGHT)/2 - 0.1*WIDTH

    if left < x < left + length and top < y < top + height:
        return True
    else:
        return False        

def drawTile(centerCoords: tuple[float, float], tileFilename: str) -> None:
    tile: pygame.Surface = pygame.image.load(tileFilename)
    tileRect: pygame.Rect = tile.get_rect()
    tileRect.center = centerCoords
    screen.blit(tile, tileRect)

def drawText(centerCoords: tuple[float, float], message: str, mode: Literal["big", "medium", "small"]) -> None:
    text: pygame.Surface
    match mode:
        case "big":
            text = bigText.render(message, True, WHITE)
        case "medium":
            text = mediumText.render(message, True, WHITE)
        case "small":
            text = smallText.render(message, True, WHITE)
        case _:
            text = smallText.render(message, True, WHITE)

    textRect: pygame.Rect = text.get_rect()
    textRect.center = centerCoords
    screen.blit(text, textRect)

def filenameAdjusted(filename: str, adjustment: str) -> str:
    filenameParts = filename.split("/")
    filenameParts[-2] += adjustment
    filenameAdjusted = "/".join(filenameParts)
    return filenameAdjusted

def isPointingAtBoard(x: int, y: int) -> bool:
    startXPos: float = 0.5 * WIDTH - 0.35 * HEIGHT
    endXPos: float = 0.5 * WIDTH + 0.35 * HEIGHT
    startYPos: float = 0.15 * HEIGHT
    endYPos: float = 0.85 * HEIGHT
    if startXPos <= x <= endXPos and startYPos <= y <= endYPos:
        return True
    else:
        return False
    
def resizeFolderImages(folderPath: str, size: tuple[int, int], adjustment: str) -> None:
    for (dir_path, dir_names, file_names) in os.walk(folderPath):
        for fileName in file_names:
            if fileName.split(".")[-1] != "png":
                continue
            imagePath: str = os.path.join(folderPath, fileName)
            imageRaw: pygame.Surface = pygame.image.load(imagePath)
            imageResized: pygame.Surface = pygame.transform.scale(imageRaw, size)
            newFolderPath = folderPath + adjustment
            os.mkdir(newFolderPath) if not os.path.exists(newFolderPath) else None
            path: str = os.path.join(newFolderPath, fileName)
            with open(path, "w") as f:
                pygame.image.save(imageResized, path)
                f.close()

def tilePointingAtBoard(x: int, y: int) -> tuple[int, int]:
    """Returns tuple (col, row) of the board tile the player is pointing at."""
    startXPos: float = 0.5 * WIDTH - 0.35 * HEIGHT
    startYPos: float = 0.15 * HEIGHT
    gridLength: float = 0.7 * HEIGHT / 15

    relativeX: float = x - startXPos
    relativeY: float = y - startYPos
    
    col: int = int(relativeX / gridLength)
    row: int = int(relativeY / gridLength)
    return col, row

def letterToTileFilename(letter: str, key: int, isBoardSize: bool) -> str:
    folderPath: str
    if isBoardSize:
        folderPath = "TileImagesBoard"
    else:
        folderPath = "TileImagesRack"

    for (dir_path, dir_names, file_names) in os.walk(folderPath):
        if letter == "BLANK":
            return "Blank1.png"
        fileNamesSorted: list = list(filter(lambda x: x[0] == letter, file_names))
        numberOfPossibleTiles: int = len(fileNamesSorted)
        # getting a variant of a tile from a hashing function - hash keys are the (row, col) postition tuples
        index: int = (key + 7) % numberOfPossibleTiles
        tileFilename: str = fileNamesSorted[index]
        return tileFilename

def highlightTileFrameRack(xRack: int, yRack: int, index: Literal[0, 1, 2, 3, 4, 5, 6], color: tuple[int, int, int], player: Player) -> None:
    numberOfTiles: int = player.getNumberOfTiles()
    if index >= numberOfTiles:
        return

    rackLength: float = 0.2 * WIDTH + 24
    rackHeight: float = rackLength / 7 + 10
    tileSide: float = rackLength / 7

    xStart: int = xRack + index * tileSide
    yStart: int = yRack
    rect: pygame.Rect = pygame.Rect(xStart, yStart, tileSide, rackHeight)
    pygame.draw.rect(screen, color, rect, width=3)

def isGameFinished(letterBag: LetterBag, numberOfMovesSkipped: int) -> bool:
    if letterBag.isEmpty():
        return True
    if numberOfMovesSkipped >= 4:
        return True
    return False

# Main game
def launchGame() -> None:
    pygame.display.set_caption("Atomic Scrabble")

    clock: pygame.time.Clock = pygame.time.Clock()

    board: Board = Board()
    
    # Initialize main objects
    letterBag: LetterBag = LetterBag()
    """
    player1: Player = Player()
    player2: Player = Player()
    player3: Player = Player()
    player4: Player = Player()
    """
    players: list[Player] = []
    numberOfPlayers: int = 4
    numberOfBots: int = 2
    for _ in range(numberOfPlayers - numberOfBots):
        players.append(Player())
    for _ in range(numberOfBots):
        players.append(Bot())
    for player in players:
        player.takeLetters(letterBag)
    playerQueue: PlayerQueue = PlayerQueue(players)
    playerCurrent: Player | Bot = players[0]
    players[-1].switchActive()
    numberOfRotations: int = random.randint(numberOfPlayers, numberOfPlayers + numberOfPlayers - numberOfBots)
    for _ in range(numberOfRotations):
        playerCurrent = playerQueue.rotate()

    # Initialize flags
    running: bool = True
    isHighlighted: bool = False
    isExchangingTiles: bool = False
    highlightedTileParams: dict = {}
    letterPlacing: str = " "
    tileExchanging: str = " "
    numberOfMovesSkipped: int = 0
    turn: Turn = Turn()

    while running:
        screen.fill(GREENPOOL)

        if playerCurrent.isBot():
            successful = playerCurrent.makeTurn(board)
            if not successful:
                playerCurrent.takeLetters(letterBag)
                playerCurrent = playerQueue.rotate()
                isExchangingTiles = False
                tileExchanging = ' '

        if isGameFinished(letterBag, numberOfMovesSkipped):
            for player in players:
                if len(player.getLetters()) == 0 and letterBag.isEmpty():
                    

        for event in pygame.event.get():
            # Quit game if top left "x" pressed
            if event.type == pygame.QUIT:
                running = False
            # Managing pressed keys
            elif event.type == pygame.KEYDOWN:
                # Quit game if "esc" key pressed
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif pygame.mouse.get_pressed()[0] == True:
                x, y = pygame.mouse.get_pos()
                col, row = tilePointingAtBoard(x, y)

                if (col, row) in turn.getTurn():
                    letterRemoving = board.getBoardElements()[row][col]
                    board.removeLetter(col, row)
                    turn.remove((col, row))
                    playerCurrent.addLetter(letterRemoving)

                    if board.isValid() and turn.isValid():
                        temporaryScore = turn.calculateScore(board)
                    else:
                        temporaryScore = 0
                    playerCurrent.setTemporaryScore(temporaryScore)

                # place letter tiles at the cursor position if a letter is selected
                if isPointingAtBoard(x, y) and playerCurrent.isPlacingLetter():
                    playerCurrent.placeLetter(letterPlacing, col, row, board)
                    turn.add((col, row))
                    letterPlacing = ""
                    playerCurrent.switchLetterPlacement()
                    isHighlighted = False

                    if board.isValid() and turn.isValid():
                        temporaryScore = turn.calculateScore(board)
                    else:
                        temporaryScore = 0
                    playerCurrent.setTemporaryScore(temporaryScore)

                    # skipping 3 frames, so that the tile is not deleted immediately
                    time.sleep(3 / 60)
                
                # End of turn button press handling
                if isPointingAtFinishButton(x, y):
                    if board.isValid() and turn.isValid():
                        playerCurrent.adjustScore(playerCurrent.getTemporaryScore())
                        temporaryScore = 0
                        playerCurrent.setTemporaryScore(temporaryScore)
                        playerCurrent.takeLetters(letterBag)
                        playerCurrent = playerQueue.rotate()
                        turn.refresh()
                # Exchanging tiles button press handling
                if isPointingAtExchangeButton(x, y):
                    # Second press
                    if isExchangingTiles:
                        #TODO
                        if len(playerCurrent.getLetters()) == startingNumberOfLetters:
                            numberOfMovesSkipped += 1
                        else:
                            numberOfMovesSkipped = 0
                        playerCurrent.takeLetters(letterBag)
                        playerCurrent = playerQueue.rotate()
                        isExchangingTiles = False
                        tileExchanging = ' '
                        time.sleep(10 / 60)
                        continue
                    # First press
                    if len(turn.getTurn()) == 0:
                        isExchangingTiles = True
                        startingNumberOfLetters = len(playerCurrent.getLetters())

                # select a letter at the current player's rack
                rackIndex: int = rackPointingAt(x, y)
                if rackIndex != 0 and playerCurrent.getId() == rackIndex:
                    i: int = (rackIndex - 1) % 2
                    j: int = (rackIndex - 1) // 2
                    xRack, yRack = rackPosition(i, j)
                    tileIndex: int = tilePointingAtRack(x, xRack)
                    numberOfLettersAvailable: int = playerCurrent.getNumberOfTiles()
                    if tileIndex <= numberOfLettersAvailable - 1:
                        isTheSameLetter = (letterPlacing == playerCurrent.getLetters()[tileIndex])
                        letterPlacing = playerCurrent.getLetters()[tileIndex]
                        if isExchangingTiles:
                            tileExchanging = letterPlacing
                        else:
                            playerCurrent.switchLetterPlacement()
                            if isTheSameLetter:
                                isHighlighted = not isHighlighted
                            else:
                                isHighlighted = True
                            highlightedTileParams["xRack"] = xRack
                            highlightedTileParams["yRack"] = yRack
                            highlightedTileParams["index"] = tileIndex
                            highlightedTileParams["color"] = (255, 0, 0)
                            highlightedTileParams["player"] = playerCurrent
        if isExchangingTiles:
            isHighlighted = False
            if tileExchanging != " ":
                playerCurrent.removeLetter(tileExchanging)
                letterBag.returnLetter(tileExchanging)
                tileExchanging = " "

        # Draws board and player racks
        drawBoard(board)
        drawRacks(playerQueue)
        # Draws finish and exchange button
        drawFinishTurnButton()
        drawExchangeTilesButton(isExchangingTiles)

        if isHighlighted and letterPlacing:
            highlightTileFrameRack(highlightedTileParams["xRack"], 
                           highlightedTileParams["yRack"], 
                           highlightedTileParams["index"],
                           highlightedTileParams["color"], 
                           highlightedTileParams["player"])
        
        # Displaying some useful info
        
        x, y = pygame.mouse.get_pos()
        if True:
            info1 = bigText.render(f"Tiles left in the bag: {letterBag.numberOfLettersRemaining()}", True, WHITE)
            infoRect = info1.get_rect()
            infoRect.center = (WIDTH/2, 0.95*HEIGHT)
            screen.blit(info1, infoRect)

        title = bigText.render("Atomic Scrabble", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = (WIDTH/2, 0.05*HEIGHT)
        screen.blit(title, titleRect)

        pygame.display.flip()
        
        clock.tick(60)  # sets FPS to 60

    pygame.quit()


if __name__ == "__main__":
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    bigText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 50)
    mediumText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 35)
    smallText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 20)

    launchGame()