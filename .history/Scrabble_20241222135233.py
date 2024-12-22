import pygame
import os
import random
import time
import json
from typing import Iterable, Literal
from numpy import transpose
from pprint import pprint
import sys
#from wordCheck import isWord
from dawg import Trie, listToStr, load
from copy import deepcopy

# RGB color constants for UI elements
WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
RED: tuple = (255, 0, 0)
ORANGEDARK: tuple = (139, 64, 0)
AMARANTH: tuple = (159, 43, 104)
GREENPOOL: tuple = (10, 108, 3)
BROWNDARK: tuple = (92, 64, 51)
BROWNLIGHT: tuple = (196, 164, 132)

# Board dimensions and resolution
WIDTH = 1470
HEIGHT = 829

# Dictionary of letter scores
LETTERS_SCORES: dict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, 
                        "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, 
                        "O": 1, "P": 3, "Q": 10,"R": 1, "S": 1, "T": 1, "U": 1, 
                        "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "BLANK": 0}

# Trie structure for word checking
"""
trie = Trie()

with open("MyDictionary.json", "r") as f:
    words = json.load(f)
    f.close()

trie = Trie()
trie.assemble(words)
"""

trie = load(/Users/MOPOLLIKA/Scrabble_NEA/trie.pkl)

def isWord(word: str) -> bool:
    """Checks if a given string is a valid word according to the trie."""
    return trie.bashSearch(word)

class Highlighters:
    """Defines ANSI escape codes for colored and styled terminal text output."""
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
    """Wraps the provided text with ANSI highlight codes."""
    return highlighting + text + Highlighters.ENDC

def indicateTile(tileType: str) -> str:
    """Returns highlighted tile type text for terminal display."""
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
    """Returns letter score multiplier based on tile type."""
    match tileType:
        case "DL":
            return 2
        case "TL":
            return 3
        case _:
            return 1

def wordMultiplicator(tileType: str) -> int:
    """Returns word score multiplier based on tile type."""
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
    """Transforms a dict of letters and counts into a flat list of letters."""
    result: list = []
    for letter, numberOfLetters in dct.items():
        result += [letter for _ in range(numberOfLetters)]
    return result

class LetterBag:
    """Manages the pool of available letters, provides methods to draw, return, and refresh letters."""
    def __init__(self) -> None:
        """Initializes the letter bag with the standard Scrabble letter distribution."""
        self.__bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, 
                      "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, 
                      "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, 
                      "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}
    
    def __repr__(self) -> str:
        # Returns a string representation of the remaining letters in the bag.
        return f"Letters left: {self.__bag}"
    
    def refresh(self) -> None:
        """Resets the letter bag to the initial letter distribution."""
        self.__bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, 
                      "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, 
                      "O": 8, "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, 
                      "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}
    
    def isEmpty(self) -> bool:
        """Checks if the letter bag has no letters left."""
        for value in self.__bag.values():
            if value != 0:
                return False
        return True
    
    def numberOfLettersRemaining(self) -> int:
        """Returns the total number of letters still in the bag."""
        return sum(self.__bag.values())
    
    def getLetter(self) -> str:
        """Draws a random letter from the bag, returns it, and removes it from the bag."""
        if not self.isEmpty():
            lettersTransformed: list = lettersTransform(self.__bag)
            index = random.randint(0, len(lettersTransformed) - 1)
            letter: str = lettersTransformed.pop(index)
            self.__bag[letter] -= 1
            return letter
        else:
            return "No letters left in the letter bag"
        
    def returnLetter(self, letter: str) -> None:
        """Returns a letter to the bag, increasing its count."""
        self.__bag[letter] += 1

# Board tile code meanings:
# LR - letter regular, DL - double letter, TL - triple letter, DW - double word, 
# TW - triple word, ST - starting point
class Board:
    """Represents the Scrabble board, holding tile placements, tile types, and validity checks."""
    def __init__(self) -> None:
        """Initializes an empty 15x15 board and sets up special tile types."""
        self.__board: list[list[str]] = [[" " for _ in range(15)] for _ in range(15)]
        self.__boardTypes: list[list[str]] = [["LR" for _ in range(15)] for _ in range(15)]
        self.__isFirstTurn: bool = True
        # Initializing tile types
        for row in range(15):
            for col in range(15):
                if (col in {0, 7, 14} and row in {0, 7, 14}) and not (col == 7 and row == 7):
                    self.__boardTypes[row][col] = "TW"
                elif (col in {3, 11} and row in {0, 7, 14}) or (col in {0, 7, 14} and row in {3, 11}) or\
                (col in {6, 8} and row in {2, 6, 8, 12}) or (col in {2, 12} and row in {6, 8}):
                    self.__boardTypes[row][col] = "DL"
                elif (col in {1, 13} and row in {1, 13}) or (col in {2, 12} and row in {2, 12}) or\
                (col in {3, 11} and row in {3, 11}) or (col in {4, 10} and row in {4, 10}):
                    self.__boardTypes[row][col] = "DW"
                elif (col in {5, 9} and row in {1, 5, 9, 14}) or (col in {1, 13} and row in {5, 9}):
                    self.__boardTypes[row][col] = "TL"
        self.__boardTypes[7][7] = "ST"
    
    
    def __repr__(self) -> str | None:
        # Prints a textual representation of the board for debugging.
        for rowElements in self.__board:
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
        """Prints the board tile types with highlighting for debugging."""
        for rowElements in self.__boardTypes:
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
        """Places a letter tile at a specified position if the cell is empty."""
        if self.__board[row][col] != " ":
            return 
        self.__board[row][col] = letter

    def removeLetter(self, col: int, row: int) -> None:
        """Removes a letter from a specified position."""
        self.__board[row][col] = " "
        
    def searchForWords(self) -> list:
        """Searches and returns a list of all valid words currently formed on the board."""
        wordsFound: list = []
        for rowElements in self.__board: 
            wordsFound += findWordsInRow(rowElements)[0]
        for colElements in transpose(self.__board):
            colElements = list(colElements)
            wordsFound += findWordsInRow(colElements)[0]
        return wordsFound
    
    def isValid(self) -> bool:
        """Checks board validity:
        - All newly formed words must be valid words.
        - On the first turn, a letter must cover the starting tile."""
        valid = isBoardValid(self.__board)
        if self.__isFirstTurn:
            if self.__board[7][7] == " ":
                return False
        return valid
    
    def fitWord(self, word: str) -> list[tuple]:
        """Attempts to place a given word on the board, returning a list of moves (col,row,letter).
        Returns empty list if not possible."""
        for row in range(15):
            for col in range(15):
                boardLetter = self.__board[row][col]
                if boardLetter not in word:
                    continue

                # Check horizontally
                left: list = scanLeft(col, row, self.__board)
                right: list = scanRight(col, row, self.__board)
                horizontalWord: str = listToStr(left) + boardLetter + listToStr(right)

                # Check vertically
                up: list = scanUp(col, row, self.__board)
                down: list = scanDown(col, row, self.__board)
                verticalWord: str = listToStr(up) + boardLetter + listToStr(down)

                # Determine placement direction
                horizontal = isWord(horizontalWord)
                vertical = isWord(verticalWord)
                stepX = 0
                stepY = 0
                if horizontal and not vertical:
                    stepY = 1
                elif not horizontal and vertical:
                    stepX = 1
                elif horizontal and vertical:
                    if horizontalWord in word:
                        stepX = 1
                    elif verticalWord in word:
                        stepY = 1
                    else:
                        continue
                
                letterIndices = [index for index in range(len(word)) if word[index] == boardLetter]
                for letterIndex in letterIndices:
                    boardCopy = deepcopy(self.__board)
                    moves = []
                    
                    currentCol = col - letterIndex * stepX
                    currentRow = row - letterIndex * stepY

                    for letter in word:
                        if not (0 <= currentCol <= 14 and 0 <= currentRow <= 14):
                            break
                        if self.__board[currentRow][currentCol] != " ":
                            currentCol += stepX
                            currentRow += stepY
                            continue
                        boardCopy[currentRow][currentCol] = letter
                        moves.append((currentCol, currentRow, letter))
                        currentCol += stepX
                        currentRow += stepY
                    if isBoardValid(boardCopy) and moves != []:
                        return moves
        return []

    def getBoardElements(self) -> list[list[str]]:
        """Returns the current letter arrangement on the board."""
        return self.__board
    
    def getBoardTypes(self) -> list[list[str]]:
        """Returns the tile type layout of the board."""
        return self.__boardTypes

def isBoardValid(board: list[list[str]]) -> bool:
    """Checks if every placed letter on the board forms valid words (horizontally or vertically)."""
    for row in range(15):
        for col in range(15):
            letter: str = board[row][col]
            if letter == " ":
                continue
            
            # Horizontal word check
            left: list = scanLeft(col, row, board)
            right: list = scanRight(col, row, board)
            horizontalWord: str = listToStr(left) + letter + listToStr(right)
            if len(horizontalWord) != 1 and not isWord(horizontalWord):
                return False
            
            # Vertical word check
            up: list = scanUp(col, row, board)
            down: list = scanDown(col, row, board)
            verticalWord: str = listToStr(up) + letter + listToStr(down)
            if len(verticalWord) != 1 and not isWord(verticalWord):
                return False
            
            # Single isolated letter check
            if len(horizontalWord) == 1 and len(verticalWord) == 1:
                return False
    return True

def scanLeft(col: int, row: int, board: list[list[str]]) -> list:
    """Traverses left from a given position to build a word segment."""
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
    """Traverses right from a given position to build a word segment."""
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
    """Traverses upward (using transpose logic) to find vertical word segments."""
    return scanLeft(row, col, transpose(board))
    
def scanDown(col: int, row: int, board: list[list[str]]) -> list:
    """Traverses downward (using transpose logic) to find vertical word segments."""
    return scanRight(row, col, transpose(board))

def findWordsInRow(rowElements) -> tuple[list, bool]:
    """Finds valid words in a given row segment."""
    row: str = "".join(rowElements)
    words: list = [element for element in row.split(" ") if element != ""]
    isCorrect: bool = True if False not in map(lambda x: isWord(x), words) else False
    words = [word for word in words if isWord(word)]
    return words, isCorrect

class Player:
    """Represents a single player in the game, tracking letters, score, and state."""
    ID = 1

    def __init__(self) -> None:
        """Initializes a player with an ID, default name, no score, and an empty letter rack."""
        self._letters: list[str] = []
        self._score: int = 0
        self._id: int = Player.ID
        self._name: str = f"Player {self._id}"
        self._active: bool = False
        self._placingLetter: bool = False
        self._bot: bool = False
        self._temporaryScore: int = 0
        Player.ID += 1

    def __repr__(self) -> str:
        # Returns a textual representation of the player's state.
        return f"Player {self._id}, Name: {self._name}, Score: {self._score}, Letters: {self._letters}, isActive: {self._active}\n"
    
    def __eq__(self, obj) -> bool:
        """Checks equality based on player ID."""
        if self._id == obj.getId():
            return True
        else:
            return False
    
    def takeLetters(self, letterBag: LetterBag) -> None | bool:
        """Draws letters from the bag until the player has 7 letters, if possible."""
        for _ in range(7 - len(self._letters)):
            letter = letterBag.getLetter()
            if letter:
                self._letters.append(letter)
            else:
                return False, "The letter bag is empty!"
    
    def addLetter(self, letter: str) -> None:
        """Adds a single letter to the player's rack if there's space."""
        if len(self._letters) == 7:
            return
        self._letters.append(letter)

    def removeLetter(self, letter: str) -> None:
        """Removes a specific letter from the player's rack."""
        if not letter == " ":
            self._letters.remove(letter)
        
    def placeLetter(self, letter: str, col: int, row: int, board: Board) -> None:
        """Places a letter from the player's rack onto the board."""
        if not self._letters:
            return
        self._letters.remove(letter)
        board.placeLetter(col, row, letter)
    
    def _applyMoves(self, board: Board, moves: list[tuple]) -> None:
        """Applies a sequence of moves (placements) to the board for the player."""
        for col, row, letter in moves:
            self.placeLetter(letter, col, row, board)
        
    def adjustScore(self, adjustment: int) -> None:
        """Adjusts the player's score by a given amount."""
        self._score += adjustment

    def setTemporaryScore(self, score: int) -> None:
        """Sets the player's temporary score for the current turn."""
        self._temporaryScore = score

    def switchActive(self) -> None:
        """Toggles whether the player is currently active."""
        self._active = not self._active

    def switchLetterPlacement(self) -> None:
        """Toggles letter placement mode for the player."""
        self._placingLetter = not self._placingLetter

    def switchBot(self) -> None:
        """Toggles whether the player is a bot."""
        self._bot = not self._bot

    def isActive(self) -> bool:
        """Returns True if the player is currently active."""
        return self._active
    
    def isBot(self) -> bool:
        """Returns True if the player is a bot."""
        return self._bot
    
    def isPlacingLetter(self) -> bool:
        """Returns True if the player is currently placing a letter."""
        return self._placingLetter
    
    def getTemporaryScore(self) -> int:
        """Returns the player's current temporary score."""
        return self._temporaryScore
    
    def getNumberOfTiles(self) -> int:
        """Returns the number of tiles in the player's rack."""
        return len(self._letters)
    
    def getLetters(self) -> list[str]:
        """Returns the list of letters in the player's rack."""
        return self._letters
    
    def getId(self) -> int:
        """Returns the player's unique ID."""
        return self._id
    
    def getName(self) -> str:
        """Returns the player's name."""
        return self._name
    
    def getScore(self) -> int:
        """Returns the player's current score."""
        return self._score
    

class Simulation:
    """Represents a simplified setup for starting a game, handling player setup and input."""
    def __init__(self) -> None:
        """Initializes a simulation environment with a board and dynamic players."""
        self.board: Board = Board()
        self.numberOfPlayers: int
        self.players: list[Player]

    def startGame(self) -> None:
        """Starts an interactive session of Atomic Scrabble with player input."""
        print()
        print(highlight("You are playing Atomic Scrabble!", Highlighters.BOLD))
        print()
        self.numberOfPlayers = int(input("Please, select 2, 3 or 4 players: "))
        self.players = [Player() for _ in range(self.numberOfPlayers)]

        enter = input("Press enter to see your letters: ")
        while enter:
            enter = input()

        for player in self.players:
            player

class PlayerQueue:
    """Holds and manages the rotation of multiple players in turn order."""
    def __init__(self, players: Iterable[Player]):
        """Initializes a queue with the provided players."""
        self.__queue: list[Player] = [player for player in players]
        self.__originalElements: list[Player] = self.__queue.copy()
        self.__length: int = len(self.__queue)

    def __repr__(self) -> str:
        # Prints the current state of the player queue.
        print(self.__queue)
        return ""
    
    def rotate(self) -> Player:
        """Rotates turn order: last player is made inactive, first player in queue becomes active."""
        playerPrevious: Player = self.__queue[-1]
        playerPrevious.switchActive()
        playerNext: Player = self.__queue.pop(0)
        playerNext.switchActive()
        self.__queue.insert(self.__length, playerNext)
        return playerNext
    
    def getOriginalElements(self) -> list[Player]:
        """Returns the original list of players."""
        return self.__originalElements
    
    def getLength(self) -> int:
        """Returns the number of players in the queue."""
        return self.__length


class Turn:
    """Represents a single turn, tracking placed tile coordinates and calculating scores."""
    def __init__(self):
        """Initializes an empty turn (no placed tiles yet)."""
        self.__turn: list[tuple] = []
    
    def initialiseFromMoves(self, moves: list[tuple]) -> None:
        """Populates the turn using a list of moves (col, row, letter)."""
        for col, row, _ in moves:
            self.__turn.append((col, row))

    def add(self, coords: tuple["col": int, "row": int]) -> None:
        """Adds a placed tile coordinate to the turn."""
        self.__turn.append(coords)

    def remove(self, coords: tuple["col": int, "row": int]) -> None:
        """Removes a tile coordinate from the turn."""
        self.__turn.remove(coords)

    def refresh(self) -> None:
        """Clears the turn state."""
        self.__turn = []

    def isValid(self) -> bool:
        """Checks if the turn placement is in a single row or a single column."""
        if not self.__turn:
            return False
        if len(self.__turn) == 1:
            return True
        
        cols: list[int] = [col for col, _ in self.__turn]
        uniqueCols: list[int] = set(cols)
        rows: list[int] = [row for _, row in self.__turn]
        uniqueRows: list[int] = set(rows)
        if (len(uniqueCols) == 1 and len(uniqueRows) >= 1) or (len(uniqueCols) >= 1 and len(uniqueRows) == 1):
            return True
        else:
            return False

    def calculateScore(self, board: Board) -> int:
        """
        Calculates the score for all newly formed words during this turn.
        Each placed tile can form horizontal and/or vertical words. 
        Letter and word multipliers apply only for tiles placed during this turn.
        """
        score: int = 0
        usedHorizontalWords: dict[str, list[tuple]] = {}
        usedVerticalWords: dict[str, list[tuple]] = {} 
        boardElements = board.getBoardElements()
        boardTypes = board.getBoardTypes()

        for col, row in self.__turn:
            letter: str = boardElements[row][col]

            # Horizontal checks
            left: list = scanLeft(col, row, boardElements)
            right: list = scanRight(col, row, boardElements)
            horizontalWord: str = listToStr(left) + letter + listToStr(right)

            if (not isWord(horizontalWord)) or (horizontalWord in usedHorizontalWords):
                continue

            usedHorizontalWords[horizontalWord] = []
            colWord: int = col - len(left)
            rowWord: int = row
            horizontalScore: int = 0
            wordMult: int = 1
            for wordLetter in horizontalWord:
                if (colWord, rowWord) in self.__turn:
                    tileType = boardTypes[rowWord][colWord]
                else:
                    tileType = "LR"
                wordMult *= wordMultiplicator(tileType)
                letterMult = letterMultiplicator(tileType)
                usedHorizontalWords[horizontalWord].append((colWord, rowWord))
                letterScore: int = LETTERS_SCORES[wordLetter]
                horizontalScore += letterScore * letterMult
                colWord = colWord + 1
            horizontalScore *= wordMult
            score += horizontalScore

        for col, row in self.__turn:
            letter: str = boardElements[row][col]

            # Vertical checks
            up: list = scanUp(col, row, boardElements)
            down: list = scanDown(col, row, boardElements)
            verticalWord: str = listToStr(up) + letter + listToStr(down)

            if (not isWord(verticalWord)) or (verticalWord in usedVerticalWords):
                continue

            usedVerticalWords[verticalWord] = []
            colWord: int = col
            rowWord: int = row - len(up)
            verticalScore: int = 0
            wordMult: int = 1
            for wordLetter in verticalWord:
                if (colWord, rowWord) in self.__turn:
                    tileType = boardTypes[rowWord][colWord]
                else:
                    tileType = "LR"
                wordMult *= wordMultiplicator(tileType)
                letterMult = letterMultiplicator(tileType)
                usedVerticalWords[verticalWord].append((colWord, rowWord))
                letterScore: int = LETTERS_SCORES[wordLetter]
                verticalScore += letterScore * letterMult
                rowWord = rowWord + 1
            verticalScore *= wordMult
            score += verticalScore

        return score
    
    def getTurn(self) -> list[tuple]:
        """Returns the list of placed tile coordinates for this turn."""
        return self.__turn


class Bot(Player):
    """Represents a bot player with a specified difficulty, capable of making automated moves."""
    def __init__(self, difficulty: int = 0):
        """Initializes a bot with a given difficulty level."""
        super().__init__()
        self._bot = True
        self._difficulty = difficulty
        self._name = f"Bot {self._id}"

    def makeTurn(self, board: Board) -> bool:
        """
        Finds and executes an optimal move given the bot's letters and the board state.
        Returns True if a valid move was made, False if no moves found (skips turn).
        """
        optimalWords = trie.generateOptimalWord(letters=self.getLetters(), difficulty=self._difficulty)
        t = time.time()
        for optimalWord in optimalWords:
            if time.time() - t >= 15:
                return False
            moves = board.fitWord(optimalWord)
            if moves == []:
                continue
            self._applyMoves(board, moves)
            turn = Turn()
            turn.initialiseFromMoves(moves)
            score = turn.calculateScore(board)
            self.adjustScore(score)
            return True
        return False

def drawBoard(board: Board) -> None:
    """Draws the board, tiles, and grid lines on the screen."""
    sideLength: float = 0.7 * HEIGHT
    gridLength: float = sideLength / 15

    startXPos: float = 0.5 * WIDTH - 0.5 * sideLength
    endXPos: float = 0.5 * WIDTH + 0.5 * sideLength
    startYPos: float = 0.15 * HEIGHT
    endYPos: float = 0.85 * HEIGHT

    pygame.draw.rect(screen, BROWNDARK, [startXPos, startYPos, sideLength, sideLength])

    # Drawing grid lines
    for i in range(15 + 1):
        pygame.draw.line(screen, BLACK, (startXPos, startYPos + i * gridLength), (endXPos, startYPos + i * gridLength), 3)
        pygame.draw.line(screen, BLACK, (startXPos + i * gridLength, startYPos), (startXPos + i * gridLength, endYPos), 3)
    
    tileStartXPos: float = startXPos + (gridLength / 2)
    tileStartYPos: float = startYPos + (gridLength / 2)

    # Drawing board type tiles
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

    # Drawing letter tiles
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

    # Drawing row/column annotations
    for row in range(15):
        numberAnnotation: str = str(row + 1)
        xNumberLeft: float = tileStartXPos - gridLength
        xNumberRight: float = tileStartXPos + 15 * gridLength
        yTile: float = tileStartYPos + (row * gridLength)
        drawText((xNumberLeft, yTile), numberAnnotation, "small")
        drawText((xNumberRight, yTile), numberAnnotation, "small")

    for col in range(15):
        letterAnnotation: str = chr(ord("A") + col)
        xTile: float = tileStartXPos + (col * gridLength)
        yLetterUp: float = tileStartYPos - gridLength
        yLetterDown: float = tileStartYPos + 15 * gridLength
        drawText((xTile, yLetterUp), letterAnnotation, "small")
        drawText((xTile, yLetterDown), letterAnnotation, "small")

def drawRacks(playerQueue: PlayerQueue) -> None:
    """Draws all players' racks on the screen."""
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
    """Calculates the position of a player's rack based on its index."""
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
    """Determines if the mouse is pointing at any of the 4 possible player racks."""
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
    """Determines which specific tile in the rack the mouse is pointing at."""
    relativeX: int = x - xRack
    tileSide = (0.2 * WIDTH + 24) / 7
    index: int = int(relativeX / tileSide)
    return index

def drawRack(xPos: float, yPos: float, player: Player, temporaryScore: int) -> None:
    """Draws a single player's rack with their tiles and name."""
    letters: list[str] = player.getLetters()
    name: str = player.getName()
    numberOfTiles: int = player.getNumberOfTiles()

    rackLength: float = 0.2 * WIDTH + 24
    rackHeight: float = rackLength / 7 + 10
    tileSide: float = rackLength / 7

    pygame.draw.rect(screen, BROWNDARK, [xPos, yPos, rackLength, rackHeight])
    for i in range(7 + 1):
        pygame.draw.line(screen, BLACK, (xPos + i * tileSide, yPos), (xPos + i * tileSide, yPos + rackHeight - 1.5), width=3)
    pygame.draw.line(screen, BLACK, (xPos - 1, yPos), (xPos + rackLength + 1.5, yPos), width=5)
    pygame.draw.line(screen, BLACK, (xPos - 1, yPos + rackHeight - 2.5), (xPos + rackLength + 1.5, yPos + rackHeight - 2.5), width=5)
    
    nameText: pygame.Surface = mediumText.render(name, True, WHITE)
    nameTextRect = nameText.get_rect()
    nameTextRect.center = (xPos + rackLength / 2, yPos - 30)
    screen.blit(nameText, nameTextRect)

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
        isActive: bool = player.isActive()
        if isActive:
            letter: str = letters[tileIndex]
            key: int = player.getId() ** 3
            tileFilename = letterToTileFilename(letter, key, isBoardSize=False)
            tileFilename = os.path.join("TileImagesRack", tileFilename)
        else:
            tileFilename = "TileImagesRack/Blank1.png"
        drawTile((xTileStart + tileIndex * tileSide - 3, yTileStart), tileFilename)

def drawFinishTurnButton() -> None:
    """Draws the 'Finish turn' button on the screen."""
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
    """Draws the 'Exchange' tiles button, highlighting it if necessary."""
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
    """Checks if mouse coordinates are over the 'Finish turn' button."""
    length = (0.2*WIDTH + 24)/2
    height = 0.1 * HEIGHT
    top = 0.5*HEIGHT - height/2
    left = (0.5*WIDTH + 0.35*HEIGHT) + (0.5*WIDTH - 0.35*HEIGHT)/2 - 0.1*WIDTH + (0.2*WIDTH + 24)/2

    return left < x < left + length and top < y < top + height

def isPointingAtExchangeButton(x: int, y: int) -> bool:
    """Checks if mouse coordinates are over the 'Exchange' button."""
    length = (0.2*WIDTH + 24)/2
    height = 0.1 * HEIGHT
    top = 0.5*HEIGHT - height/2
    left = (0.5*WIDTH + 0.35*HEIGHT) + (0.5*WIDTH - 0.35*HEIGHT)/2 - 0.1*WIDTH

    return left < x < left + length and top < y < top + height

def drawTile(centerCoords: tuple[float, float], tileFilename: str) -> None:
    """Draws an individual tile image at the given coordinates."""
    tile: pygame.Surface = pygame.image.load(tileFilename)
    tileRect: pygame.Rect = tile.get_rect()
    tileRect.center = centerCoords
    screen.blit(tile, tileRect)

def drawText(centerCoords: tuple[float, float], message: str, mode: Literal["big", "medium", "small"]) -> None:
    """Renders and draws text at the given coordinates with a given size."""
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
    """Adjusts a filename by modifying a directory in its path."""
    filenameParts = filename.split("/")
    filenameParts[-2] += adjustment
    filenameAdjusted = "/".join(filenameParts)
    return filenameAdjusted

def isPointingAtBoard(x: int, y: int) -> bool:
    """Checks if mouse coordinates are within the board boundaries."""
    startXPos: float = 0.5 * WIDTH - 0.35 * HEIGHT
    endXPos: float = 0.5 * WIDTH + 0.35 * HEIGHT
    startYPos: float = 0.15 * HEIGHT
    endYPos: float = 0.85 * HEIGHT
    return startXPos <= x <= endXPos and startYPos <= y <= endYPos

def resizeFolderImages(folderPath: str, size: tuple[int, int], adjustment: str) -> None:
    """Resizes all png images in a folder to a specified size and saves them to a new folder."""
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
    """Determines which board cell the mouse is pointing at."""
    startXPos: float = 0.5 * WIDTH - 0.35 * HEIGHT
    startYPos: float = 0.15 * HEIGHT
    gridLength: float = 0.7 * HEIGHT / 15

    relativeX: float = x - startXPos
    relativeY: float = y - startYPos
    
    col: int = int(relativeX / gridLength)
    row: int = int(relativeY / gridLength)
    return col, row

def letterToTileFilename(letter: str, key: int, isBoardSize: bool) -> str:
    """Determines the filename for a tile image based on the letter and a key for variation."""
    folderPath: str
    if isBoardSize:
        folderPath = "TileImagesBoard"
    else:
        folderPath = "TileImagesRack"

    for (dir_path, dir_names, file_names) in os.walk(folderPath):
        if letter == "BLANK":
            return "Blank1.png"
        fileNamesSorted: list = list(filter(lambda x: x[0] == letter and x[0:5] != "Blank", file_names))
        numberOfPossibleTiles: int = len(fileNamesSorted)
        index: int = (key + 7) % numberOfPossibleTiles
        tileFilename: str = fileNamesSorted[index]
        return tileFilename

def highlightTileFrameRack(xRack: int, yRack: int, index: Literal[0, 1, 2, 3, 4, 5, 6], color: tuple[int, int, int], player: Player) -> None:
    """Highlights the selected tile in the player's rack with a colored frame."""
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
    """Checks if the game is finished (no tiles left or too many consecutive skips)."""
    if letterBag.isEmpty() and numberOfMovesSkipped >= 1:
        return True
    if numberOfMovesSkipped >= 4:
        return True
    return False

def adjustFinalScores(player: Player, players: list[Player]) -> None:
    """Adjusts final scores when the game ends and one player used all letters.
    That player gains points equal to all remaining letter values of other players.
    Other players lose the value of their leftover letters."""
    otherPlayers = [otherPlayer for otherPlayer in players if otherPlayer != player]
    scoreSum = 0
    for otherPlayer in otherPlayers:
        score = sum(map(lambda x: LETTERS_SCORES[x], otherPlayer.getLetters()))
        scoreSum += score
        otherPlayer.adjustScore(-score)
    player.adjustScore(scoreSum)

def launchGame() -> None:
    """Main game loop that initializes objects, handles events, and updates the screen."""
    pygame.display.set_caption("Atomic Scrabble")

    clock: pygame.time.Clock = pygame.time.Clock()

    board: Board = Board()

    letterBag: LetterBag = LetterBag()
    players: list[Player] = []
    numberOfPlayers: int = 4
    numberOfBots: int = 2
    botDifficulty: int = 6
    for _ in range(numberOfPlayers - numberOfBots):
        players.append(Player())
    for _ in range(numberOfBots):
        players.append(Bot(difficulty=botDifficulty))
    for player in players:
        player.takeLetters(letterBag)
    playerQueue: PlayerQueue = PlayerQueue(players)
    playerCurrent: Player | Bot = players[0]
    players[-1].switchActive()
    numberOfRotations: int = 1
    for _ in range(numberOfRotations):
        playerCurrent = playerQueue.rotate()

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
            playerCurrent.takeLetters(letterBag)
            playerCurrent = playerQueue.rotate()
            isExchangingTiles = False
            tileExchanging = ' '

        if isGameFinished(letterBag, numberOfMovesSkipped):
            for player in players:
                if len(player.getLetters()) == 0 and letterBag.isEmpty():
                    adjustFinalScores(player, players)
                    winner = max(players, key=lambda x: x.getScore())
                    print(winner + "is a winner!")
                    running = False
            if numberOfMovesSkipped >= 4:
                print(f"The game is finished! Players' scores: \n{[player for player in players]}")
                running = False
            
        for event in pygame.event.get():
            # Handle quitting
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # ESC key quits
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif pygame.mouse.get_pressed()[0] == True:
                x, y = pygame.mouse.get_pos()
                col, row = tilePointingAtBoard(x, y)

                # Remove a placed tile if clicked again on it
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

                # Place a tile on the board if in placing mode
                if isPointingAtBoard(x, y) and playerCurrent.isPlacingLetter():
                    if board.getBoardElements()[row][col] != " ":
                        continue
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
                    
                    time.sleep(3 / 60)
                
                # Finish turn button
                if isPointingAtFinishButton(x, y):
                    if board.isValid() and turn.isValid():
                        playerCurrent.adjustScore(playerCurrent.getTemporaryScore())
                        temporaryScore = 0
                        playerCurrent.setTemporaryScore(temporaryScore)
                        playerCurrent.takeLetters(letterBag)
                        playerCurrent = playerQueue.rotate()
                        turn.refresh()
                
                # Exchange button
                if isPointingAtExchangeButton(x, y):
                    # If already exchanging, finalize exchange
                    if isExchangingTiles:
                        if len(playerCurrent.getLetters()) == startingNumberOfLetters:
                            numberOfMovesSkipped += 1
                        else:
                            numberOfMovesSkipped = 0
                        playerCurrent.takeLetters(letterBag)
                        playerCurrent = playerQueue.rotate()
                        isExchangingTiles = False
                        tileExchanging = ' '
                        time.sleep(20 / 60)
                        continue
                    # Start exchanging if no tiles placed
                    if len(turn.getTurn()) == 0:
                        isExchangingTiles = True
                        startingNumberOfLetters = len(playerCurrent.getLetters())

                # Selecting a letter from rack
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
            # Exchange step: chosen tile removed from player and returned to bag
            isHighlighted = False
            if tileExchanging != " ":
                playerCurrent.removeLetter(tileExchanging)
                letterBag.returnLetter(tileExchanging)
                tileExchanging = " "

        # Draw everything
        drawBoard(board)
        drawRacks(playerQueue)
        drawFinishTurnButton()
        drawExchangeTilesButton(isExchangingTiles)

        if isHighlighted and letterPlacing:
            highlightTileFrameRack(highlightedTileParams["xRack"], 
                                   highlightedTileParams["yRack"], 
                                   highlightedTileParams["index"],
                                   highlightedTileParams["color"], 
                                   highlightedTileParams["player"])
        
        x, y = pygame.mouse.get_pos()
        # Info text
        info1 = bigText.render(f"Tiles left in the bag: {letterBag.numberOfLettersRemaining()}", True, WHITE)
        infoRect = info1.get_rect()
        infoRect.center = (WIDTH/2, 0.95*HEIGHT)
        screen.blit(info1, infoRect)

        title = bigText.render("Atomic Scrabble", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = (WIDTH/2, 0.05*HEIGHT)
        screen.blit(title, titleRect)

        pygame.display.flip()
        
        clock.tick(60)  # Limit FPS to 60

    pygame.quit()


if __name__ == "__main__":
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    bigText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 50)
    mediumText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 35)
    smallText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 20)

    launchGame()
