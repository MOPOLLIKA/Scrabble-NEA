from Scrabble import findWordsInRow

lst: list = [" ", "A", "P", "R", "I", "C", "O", " ", " ", " ", " ", "S", "E", "L", "L", " "]
dct: dict[str: float] = {"andy": "mike"}
print(dct.items())
print(findWordsInRow(lst))
