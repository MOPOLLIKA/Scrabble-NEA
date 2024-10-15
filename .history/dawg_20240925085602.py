import pickle

dawgFilename = "trie.pkl"


class Edge:
    def __init__(self, letter, leftNode, rightNode):
        ...


class Node:
    def __init__(self, edge: Edge, isTerminal: bool, isRoot: bool):
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.edges = []


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)