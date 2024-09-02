from Scrabble import findWordsInRow, Board, resizeFolderImages, resizeFolderImages, letterToTileFilename
import wordCheckAPI as wc
import pygame


def checkWordScan() -> None:
        board = Board()
        board.placeLetter(1, 2, "A")
        board.placeLetter(2, 2, "T")
        board.placeLetter(3, 2, "T")
        board.placeLetter(4, 2, "O")
        board.placeLetter(5, 2, "R")
        board.placeLetter(6, 2, "N")
        board.placeLetter(7, 2, "E")
        board.placeLetter(8, 2, "Y")

lst: list = [" ", "A", "P", "R", "I", "C", "O", " ", " ", " ", " ", "S", "E", "L", "L", " "]
dct: dict[str: int] = {"andy": 1}

WIDTH = 1470
HEIGHT = 829

boardSide: float = 0.7 * HEIGHT / 15 - 3
rackSide: float = 0.2 * WIDTH / 7 - 3
resizeFolderImages("TileImages", (rackSide, rackSide), "Rack")

letter: str = "A"
print(letterToTileFilename(letter, True))
image = pygame.image.load()