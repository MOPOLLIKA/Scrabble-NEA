from Scrabble import findWordsInRow
import wordCheckAPI as wc


lst: list = [" ", "A", "P", "R", "I", "C", "O", " ", " ", " ", " ", "S", "E", "L", "L", " "]
dct: dict[str: int] = {"andy": 1}
assert type(list(dct.items())[0][1]) == int
print(findWordsInRow(lst))
text = "TileImages/A1.png"
text = "".join(text.split(".png"))