import pickle

class Node:
    def __init__(self, letter, isTerminal, isRoot):
        self.letter = letter
        self.isTerminal = isTerminal
        self.isRoot = isRoot

def save(object, filename):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.)