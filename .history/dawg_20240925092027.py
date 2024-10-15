import pickle
from typing import Callable

dawgFilename = "trie.pkl"


class Edge:
    def __init__(self, letter, leftNode, rightNode) -> None:
        self.letter = letter
        self.leftNode = leftNode
        self.rightNode = rightNode


class Node:
    def __init__(self, isTerminal: bool, isRoot: bool, edge: Edge = None) -> None:
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.isLeaf = isLeaf
        self.leftEdge = None
        self.rightEdge = None
        if not self.isRoot:
            self.leftEdge = edge


class Trie:
    def __init__(self, rootNode: Node) -> None:
        self.rootNode = rootNode
    
    def _assemble(self, func: Callable) -> None:
        ...
    
    


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)