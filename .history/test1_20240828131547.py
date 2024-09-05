from Scrabble import findWordsInRow
import wordCheckAPI as wc


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
assert type(list(dct.items())[0][1]) == int
print(findWordsInRow(lst))
text = "TileImages/A1.png"
textParts = text.split(".")
textParts.insert(1, "Resized.")
text = "".join(textParts)
print(text)