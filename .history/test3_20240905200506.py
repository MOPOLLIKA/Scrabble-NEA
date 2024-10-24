from Scrabble import Board


board: Board = Board()
board.placeLetter(1, 1, "A")
board.placeLetter(1, 2, "D")
board.placeLetter(1, 3, "D")
board.placeLetter(2, 2, "A")
board.placeLetter(3, 2, "W")
board.placeLetter(4, 2, "N")
print(board)
print(board.searchForWords())
print(board.isValid())
print(str(["A", "b", "e"]))