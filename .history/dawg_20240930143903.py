import pickle
from typing import Callable

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
dawgFilename = "trie.pkl"


class Edge:
    def __init__(self, letter: str, leftNode, rightNode: Node) -> None:
        self.letter = letter
        self.leftNode = leftNode
        self.rightNode = rightNode

    def getLetter(self) -> str:
        return self.letter


class Node:
    def __init__(self, isTerminal: bool, isRoot: bool) -> None:
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.leftEdges: list[Edge] = []
        self.rightEdges: list[Edge] = []

    def addLeftEdge(self, edge: Edge) -> None:
        self.leftEdges.append(edge)

    def getRightEdges(self) -> list[Edge]:
        return self.rightEdges
    
    def getLeftEdges(self) -> list[Edge]:
        return self.leftEdges


class Trie:
    def __init__(self, rootNode: Node, acceptor: Callable, partialAcceptor: Callable) -> None:
        self.rootNode = rootNode
    
    def _assemble(self, vocabulary: dict[str, str]) -> None:
        lastNode = self.rootNode
        isRoot = True
        # Going through each word in the alphabet
        for word in vocabulary.keys():
            lettersUsed = ""
            for letter in word:
                lettersUsed += letter
                isTerminal = (lettersUsed == word)

                newNode = Node(isTerminal, isRoot)
                newEdge = Edge(letter, lastNode, newNode)
                newNode.addLeftEdge(newEdge)
            

    
    


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)