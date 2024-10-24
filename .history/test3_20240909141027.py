from Scrabble import Board, listToStr


board: Board = Board()
board.placeLetter(1, 1, "A")
board.placeLetter(1, 2, "D")
board.placeLetter(1, 3, "D")
board.placeLetter(2, 2, "A")
board.placeLetter(3, 2, "W")
board.placeLetter(4, 2, "N")
board.placeLetter(4, 1, "W")
board.placeLetter(4, 0, "O")
board.placeLetter(0, 3, "A")
print(board)
print(board.searchForWords())
print(board.isValid())

LETTERS_SCORES: dict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, 
                        "O": 1, "P": 3,"Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "BLANK": 0}

for letters in zip([item for item in LETTERS_SCORES.items()]):
        print(letters)
