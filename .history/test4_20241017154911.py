from copy import deepcopy
from Scrabble import Board

board = Board()
board.placeLetter(3, 3, "A")
board.placeLetter(3, 4, "P")
board.placeLetter(3, 5, "P")
board.placeLetter(3, 6, "L")
board.placeLetter(3, 7, "E")
board.placeLetter(4, 3, "D")
moves = board.fitWord("PEAR")
print(board)
print(moves)
board.applyMoves(moves)
print(board)

lst = [1, 2, 3, 4, 5]
