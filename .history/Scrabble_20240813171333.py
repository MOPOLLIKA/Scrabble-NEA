import tkinter as tk
import pygame
import wordCheckAPI as wc
from wordCheck import isWord


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


class LetterBag:
        def __init__(self) -> None:
                self.bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2,"N": 6, 
                            "O": 8, "P": 2,"Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}

        def __repr__(self) -> str:
                return f"Letters left: {self.bag}"
        
        def refresh(self) -> None:
                self.bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2,
                   "N": 6, "O": 8, "P": 2,"Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}
        
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
                for row in self.board:
                        print("|", end="")
                        print("-" * 59, end="")
                        print("|")
                        for col in row:
                                print("| ", end="")
                                print(col, end=" ")
                        print("|")
                print("|", end="")
                print("-" * 59, end="")
                print("|", end="")
                return ""
    
        def printTypes(self) -> None:
                for row in self.boardTypes:
                        print("|", end="")
                        print("-" * 74, end="")
                        print("|")
                        for col in row:
                                print("| ", end="")
                                indicatedTile = indicateTile(col)
                                print(indicatedTile, end=" ")
                        print("|")
                print("|", end="")
                print("-" * 74, end="")
                print("|", end="")
                print()
    
        def placeLetter(self, col: int, row: int, letter: str):
                if self.board[col][row] == 0:
                        self.board[col][row] = letter
                        return True
                else:
                        return False


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
            
        def placeLetter(self, index: int, col: int, row: int, board: Board):
                if self.letters:
                        return board.placeLetter(col, row, self.letters[index])
                else:
                        return False
                

class Simulation:
        def __init__(self):
                self.board: Board = Board()
                self.numberOfPlayers: int
                self.players: list[Player]

        def startGame(self):
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

        
#Main game loop
pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrabble Ultra")

clock = pygame.time.Clock()
running = True

while running:
        rect = pygame.draw.rect(screen, (0, 255, 0), [100, 100, 200, 200])
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                        
        pygame.display.flip()
        
        clock.tick(60)  # limits FPS to 60

pygame.quit()

