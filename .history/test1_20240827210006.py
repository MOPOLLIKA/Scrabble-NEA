from Scrabble import findWordsInRow

lst: list = [" ", "A", "P", "R", "I", "C", "O", " ", " ", " ", " ", "S", "E", "L", "L", " "]
dct: dict[str: float] = {"andy": 1}
print(list(dct.items())[0])
print(findWordsInRow(lst))
