import pickle
from typing import Callable

dawgFilename = "trie.pkl"


class Edge:
    def __init__(self, letter, leftNode, rightNode):
        self.letter = letter
        self.leftNode = leftNode
        self.rightNode = rightNode


class Node:
    def __init__(self, edge: Edge, isTerminal: bool, isRoot: bool):
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.leftEdge = edge
        self.rightEdge = None

def createTrie(isWord: Callable[[str], bool]) -> Node:
    """Creates a word trie from an acceptor function which determines whether a string is a word."""
    rootNode = Node()


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)