import typing as t
import collections.abc as c
import pygame
from numpy import transpose
import wordCheckAPI as wc
from wordCheck import isWord

pygame.init()

WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
GREENPOOL: tuple = (10, 108, 3)
BROWNDARK: tuple = (92, 64, 51)

WIDTH: int = 1280
HEIGHT: int = 800

screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))

bigText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 50)
mediumText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 35)
smallText: pygame.font.Font = pygame.font.Font("helvetica-neue-5/HelveticaNeueLight.otf", 20)

LETTERS_SCORES: dict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, 
                        "O": 1, "P": 3,"Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "BLANK": 0}

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
        
        def getLetter(self) -> str | bool:
                if not self.isEmpty():
                        lettersAvailable = set(filter(lambda x: self.bag[x] != 0, self.bag.keys()))
                        letter = lettersAvailable.pop()
                        self.bag[letter] =- 1
                        return letter
                else:
                        return False
                
        def returnLetter(self, letter: str) -> None:
                self.bag[letter] += 1

# LR - letter, DL - double letter, TL - triple letter,  DW - double word, TW - triple word, ST - start point
class Board:
        def __init__(self) -> None:
                self.board = [[" " for _ in range(15)] for _ in range(15)]
                self.boardTypes = [["LR" for _ in range(15)] for _ in range(15)]
                self.bag = LetterBag()
                # initialise tile types
                for row in range(15):
                        for col in range(15):
                                if col in {0, 7, 14} and row in {0, 7, 14} and (col != 7 and row != 7):
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
    
        def placeLetter(self, col: int, row: int, letter: str) -> bool:
                if self.board[col][row] == " ":
                        self.board[col][row] = letter
                        return True
                else:
                        return False
                
        def searchForWords(self) -> list:
                wordsFound: list = []
                for rowElements in self.board:
                        wordsFound += findWordsInRow(rowElements)[0]
                for colElements in transpose(self.board):
                        colElements = list(colElements)
                        wordsFound += findWordsInRow(colElements)[0]
                return wordsFound

def findWordsInRow(rowElements) -> tuple[list, bool]:
        row: str = "".join(rowElements)
        words: list = [element for element in row.split(" ") if element != ""]
        isCorrect: bool = True if False not in map(lambda x: isWord(x), words) else False
        words = [word for word in words if isWord(word)]
        return words, isCorrect
                                        

class Player:
        ID = 1

        def __init__(self) -> None:
                self.letters = []
                self.score = 0
                self.id = Player.ID
                self.name = input(f"Please enter Player {self.id} name: ")
                Player.ID += 1

        def __repr__(self) -> str:
                return f"Player {self.id}\nName: {self.name}\nScore: {self.score}\nLetters: {self.letters}\n"
    
        def takeLetters(self, letterbag: LetterBag):
                for _ in range(7 - len(self.letters)):
                        letter = letterbag.getLetter()
                        if letter:
                                self.letters.append(letter)
                        else:
                                return False, "The letter bag is empty!"
            
        def placeLetter(self, letter: str, col: int, row: int, board: Board) -> None | bool:
                if self.letters:
                        return board.placeLetter(col, row, letter)
                else:
                        return False
                

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


def drawBoard() -> None:
        sideLength: float = 0.8 * HEIGHT
        gridLength: float = sideLength / 15

        startXPos: float = 0.5 * WIDTH - 0.5 * sideLength
        endXPos: float = 0.5 * WIDTH + 0.5 * sideLength
        startYPos: float = 0.1 * HEIGHT
        endYPos: float = 0.9 * HEIGHT

        pygame.draw.rect(screen, BROWNDARK, [startXPos, startYPos, sideLength, sideLength])

        # drawing grid
        for i in range(15 + 1):
                pygame.draw.line(screen, BLACK, (startXPos, startYPos + i * gridLength), (endXPos, startYPos + i * gridLength), 3) # horizontal
                pygame.draw.line(screen, BLACK, (startXPos + i * gridLength, startYPos), (startXPos + i * gridLength, endYPos), 3) # vertical    

def drawRacks(names: dict[str: int]) -> None:
        """Variable `names` is in the following format: {'name1': numberOfTiles1, 'name2': numberOfTiles2, ...}"""
        height: float = 0.2 * HEIGHT
        length: float = 0.4 * WIDTH

        count: int = len(names)
        for i in range(2):
                for j in range(2):
                        if count == 0:
                                break

                        xPos, yPos = rackPosition(i, j)
                        
                        index: int = 2 * i + j
                        numberOfTiles: int = list(names.items())[index - 1][1]
                        drawRack(xPos, yPos, index, numberOfTiles)

                        count -= 1

def rackPosition(i: int, j: int) -> tuple[int, int]:
        if i == 1:
                yPos = 0.1 * HEIGHT
        else:
                yPos = 0.9 * HEIGHT

        if j == 1:
                xPos = 0.1 * WIDTH
        else:
                xPos = 0.9 * WIDTH
        return xPos, yPos
        
def drawRack(xPos: float, yPos: float, index: int, numberOfTiles: int) -> None:
        pygame.rect()


# Main game
def launchGame() -> None:
        pygame.display.set_caption("Scrabble Ultra")

        clock: pygame.time.Clock = pygame.time.Clock()
        running: bool = True

        while running:

                screen.fill(GREENPOOL)

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False
                
                drawBoard()

                pygame.display.flip()
                
                clock.tick(60)  # sets FPS to 60

        pygame.quit()


if __name__ == "__main__":
        board = Board()
        board.placeLetter(1, 2, "A")
        board.placeLetter(2, 2, "T")
        board.placeLetter(3, 2, "T")
        board.placeLetter(4, 2, "O")
        board.placeLetter(5, 2, "R")
        board.placeLetter(6, 2, "N")
        board.placeLetter(7, 2, "E")
        board.placeLetter(8, 2, "Y")
        board.printTypes()
        print(board.searchForWords())
        import sys; sys.exit()
        launchGame()