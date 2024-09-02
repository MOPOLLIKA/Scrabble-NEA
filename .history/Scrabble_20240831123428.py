import pygame
from numpy import transpose
from math import floor
import wordCheckAPI as wc
from wordCheck import isWord

pygame.init()

WHITE: tuple = (255, 255, 255)
BLACK: tuple = (0, 0, 0)
GREENPOOL: tuple = (10, 108, 3)
BROWNDARK: tuple = (92, 64, 51)
BROWNLIGHT: tuple = (196, 164, 132)
# 1470:956 - the real resolution, 1280:800 - the chosen resolution
WIDTH = 1470
HEIGHT = 829

screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

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
        
        def getBoardElements(self) -> list[list[str]]:
                return self.board
    
        def placeLetter(self, col: int, row: int, letter: str) -> bool:
                if self.board[row][col] == " ":
                        self.board[row][col] = letter
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
    
        def takeLetters(self, letterbag: LetterBag) -> None | bool:
                for _ in range(7 - len(self.letters)):
                        letter = letterbag.getLetter()
                        if letter:
                                self.letters.append(letter)
                        else:
                                return False, "The letter bag is empty!"
            
        def placeLetter(self, letter: str, col: int, row: int, board: Board) -> bool:
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

        tiles = board.getBoardElements()
        for row in range(15):
                for col in range(15):
                        letter = tiles[row][col]
                        pass #TODO

def drawRacks(names: dict[str: int]) -> None:
        """Variable `names` is in the following format: {'name1': numberOfTiles1, 'name2': numberOfTiles2, ...}"""
        count: int = len(names)
        for i in range(2):
                for j in range(2):
                        if count == 0:
                                break

                        xPos, yPos = rackPosition(i, j)
                        
                        index: int = 2 * i + j
                        name, numberOfTiles = list(names.items())[index - 1]
                        drawRack(xPos, yPos, name, numberOfTiles)

                        count -= 1

def rackPosition(i: int, j: int) -> tuple[float, float]:
        rackLength: float = 0.2 * WIDTH
        rackHeight: float = rackLength / 7 + 10
        if i == 0:
                yPos: float = 0.2 * HEIGHT
        else:
                yPos: float = 0.8 * HEIGHT - rackHeight

        if j == 0:
                xPos: float = (0.5 * WIDTH - 0.35 * HEIGHT) / 2 - 0.1 * WIDTH
        else:
                xPos: float = (0.5 * WIDTH + 0.35 * HEIGHT) + (0.5 * WIDTH - 0.35 * HEIGHT) / 2 - 0.1 * WIDTH
        return xPos, yPos
        
def drawRack(xPos: float, yPos: float, name: str, numberOfTiles: int) -> None:
        rackLength: float = 0.2 * WIDTH + 24
        rackHeight: float = rackLength / 7 + 10
        tileSide: float = rackLength / 7

        # Rack surface
        pygame.draw.rect(screen, BROWNLIGHT, [xPos, yPos, rackLength, rackHeight])
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

        scoreText: pygame.Surface = mediumText.render(f"Score: {0}", True, WHITE)
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.center = (xPos + rackLength / 2, yPos + rackHeight + 30)
        screen.blit(scoreText, scoreTextRect)

        tileSide = tileSide - (24 / 7)
        blankTileFilename: str = "TileImages/X1.png"
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
                xTile: float = xTileStart + tileIndex * (tileSide + 3)
                drawTile(xTile, yTileStart, blankTileFilename, isBoardSize=False)

def drawTile(x: float, y: float, tileFilename: str, isBoardSize: bool = True) -> None:
        if isBoardSize:
                boardGridLength: float = 0.7 * HEIGHT / 15
                side: float = boardGridLength - 3       # accounting for black lines
        else:
                side: float = 0.2 * WIDTH / 7
        tileRaw: pygame.Surface = pygame.image.load(tileFilename)
        tile: pygame.Surface = pygame.transform.scale(tileRaw, (side, side))
        tileRect: pygame.Rect = tile.get_rect()
        tileRect.center = (x, y)
        screen.blit(tile, tileRect)

def filenameAdjusted(filename: str, adjustment: str) -> str:
        filenameParts = filename.split("/")
        filenameParts.insert(1, f"{adjustment}/")
        filenameResized = "".join(filenameParts)
        return filenameResized

def isPointingAtBoard(x: int, y: int) -> bool:
        startXPos: float = 0.5 * WIDTH - 0.35 * HEIGHT
        endXPos: float = 0.5 * WIDTH + 0.35 * HEIGHT
        startYPos: float = 0.15 * HEIGHT
        endYPos: float = 0.85 * HEIGHT
        if startXPos <= x <= endXPos and startYPos <= y <= endYPos:
                return True
        else:
                return False
        
def 

def tilePointingAt(x: int, y: int) -> tuple[int, int]:
        """Returns tuple (col, row) of the board tile the player is pointing at."""
        startXPos: float = 0.5 * WIDTH - 0.35 * HEIGHT
        startYPos: float = 0.15 * HEIGHT
        gridLength: float = 0.7 * HEIGHT / 15

        relativeX: float = x - startXPos
        relativeY: float = y - startYPos
        
        col: int = floor(relativeX / gridLength)
        row: int = floor(relativeY / gridLength)
        return col, row

# Main game
def launchGame() -> None:
        pygame.display.set_caption("Scrabble Ultra")

        clock: pygame.time.Clock = pygame.time.Clock()

        board: Board = Board()
        players: list[Player]
        playerCurrent: Player = Player()

        # Initialize flags
        running: bool = True
        isPlacingLetter: bool = True

        title = bigText.render("Scrabble Ultra", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = (WIDTH / 2, 0.1 * HEIGHT)

        while running:

                screen.fill(GREENPOOL)
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
                                if isPointingAtBoard(x, y):
                                        col, row = tilePointingAt(x, y)
                                        if isPlacingLetter:
                                                board.placeLetter(col, row, "A")
                                                print(board)
                
                drawBoard(board)
                drawRacks({"Oliver": 7, "Michael": 3, "Oscar": 4, "Cole": 7})
                
                # Displaying some useful info
                x, y = pygame.mouse.get_pos()
                info = bigText.render(f"{tilePointingAt(x, y)}", True, WHITE)
                infoRect = info.get_rect()
                infoRect.center = (WIDTH / 2, HEIGHT / 2)
                screen.blit(info, infoRect)

                screen.blit(title, titleRect)

                pygame.display.flip()
                
                clock.tick(60)  # sets FPS to 60

        pygame.quit()


if __name__ == "__main__":
        #import sys; sys.exit()
        launchGame()