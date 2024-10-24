from Scrabble import Board


board: Board = Board()
board.placeLetter(1, 1, "A")
board.placeLetter(1, 2, "D")
board.placeLetter(1, 3, "D")
board.placeLetter(1, 1, "A")
board.placeLetter(1, 1, "A")
print(board)
print(board.searchForWords())