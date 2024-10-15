import pickle
from typing import Callable

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FILENAME = "trie.pkl"


class Edge:
    def __init__(self, letter: str, leftNode, rightNode) -> None:
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
    def __init__(self, rootNode: Node) -> None:
        self.rootNode = rootNode
    
    def _assemble(self, vocabulary: dict[str, str]) -> None:
        newNode = self.rootNode
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
                last

    def isTrieWord(self, word: str) -> bool:
        lastNode = 
        for letter in word:
            
            

    
    


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)