from Scrabble import findWordsInRow, Board, resizeFolderImages, resizeFolderImages, letterToTileFilename
import wordCheckAPI as wc
import pygame
import os


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
resizeFolderImages("TileImages", (boardSide, boardSide), "Board")
""""""
letter: str = "A"
path = letterToTileFilename(letter, True)
image: pygame.Surface = pygame.image.load(os.path.join("TileImages", path))
pygame.image.save(image, "TileImages/ 1.png")
"""