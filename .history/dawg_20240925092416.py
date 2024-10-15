import pickle
from typing import Callable

alphabet = "abcdefghijklmnopqrstuvwxyz"
dawgFilename = "trie.pkl"


class Edge:
    def __init__(self, letter, leftNode, rightNode) -> None:
        self.letter = letter
        self.leftNode = leftNode
        self.rightNode = rightNode


class Node:
    def __init__(self, isTerminal: bool, isRoot: bool, isLeaf: bool, edge: Edge = None) -> None:
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.isLeaf = isLeaf
        self.leftEdge = None
        self.rightEdge = None
        if not self.isRoot:
            self.leftEdge = edge


class Trie:
    def __init__(self, rootNode: Node, acceptor: Callable) -> None:
        self.rootNode = rootNode
        self.acceptor = acceptor
    
    def _assemble(self, lastNode) -> None:
        currentWord = 
        for letter in alphabet:
            if 
        
    
    


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)