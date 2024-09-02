from Scrabble import findWordsInRow
import wordCheckAPI as wc


def checkWords

lst: list = [" ", "A", "P", "R", "I", "C", "O", " ", " ", " ", " ", "S", "E", "L", "L", " "]
dct: dict[str: int] = {"andy": 1}
assert type(list(dct.items())[0][1]) == int
print(findWordsInRow(lst))
text = "TileImages/A1.png"
textParts = text.split(".")
textParts.insert(1, "Resized.")
text = "".join(textParts)
print(text)