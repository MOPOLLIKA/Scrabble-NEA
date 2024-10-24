from Scrabble import Board, Turn, listToStr, lettersTransform


board: Board = Board()
turn: Turn = Turn()
board.placeLetter(7, 7, "A")
turn.add((7, 7))
board.placeLetter(7, 8, "D")
turn.add((7, 8))
board.placeLetter(7, 9, "D")
turn.add((7, 9))
board.placeLetter(6, 9, "D")
turn.add((6, 9))

print(board)
board.printTypes()
print(board.searchForWords())
print(board.isValid())

LETTERS_SCORES: dict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, 
                        "O": 1, "P": 3,"Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "BLANK": 0}

bag = {"A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9, "J": 1, "K": 1, "L": 4, "M": 2,"N": 6, 
                "O": 8, "P": 2,"Q": 1, "R": 6, "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 4, "BLANK": 2}

print(turn.calculateScore(board))
