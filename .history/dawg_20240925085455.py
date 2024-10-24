import pickle

dawgFilename = "trie.pkl"

class Node:
    def __init__(self, letter, isTerminal, isRoot):
        self.letter = letter
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.edges = []
    

class Edge:
    def __init__(self, )

def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)