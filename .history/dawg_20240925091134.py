import pickle
from typing import Callable

dawgFilename = "trie.pkl"


class Edge:
    def __init__(self, letter, leftNode, rightNode) -> None:
        self.letter = letter
        self.leftNode = leftNode
        self.rightNode = rightNode
        return 


class Node:
    def __init__(self, isTerminal: bool, isRoot: bool, edge: Edge = None) -> None:
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.leftEdge = None
        self.rightEdge = None
        if not self.isRoot:
            self.leftEdge = edge


class Trie:
    def __init__(self, func: Callable) -> None:
        self.acceptor = func


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)