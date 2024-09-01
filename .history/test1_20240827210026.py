from Scrabble import findWordsInRow

lst: list = [" ", "A", "P", "R", "I", "C", "O", " ", " ", " ", " ", "S", "E", "L", "L", " "]
dct: dict[str: int] = {"andy": 1}
list(dct.items())[0][1]
print(findWordsInRow(lst))
