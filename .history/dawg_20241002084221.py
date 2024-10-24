import pickle
from platform import node
from typing import Callable

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FILENAME = "trie.pkl"


class Edge:
    def __init__(self, letter: str, leftNode, rightNode) -> None:
        self.letter = letter
        self.leftNode: Node = leftNode
        self.rightNode = rightNode
        leftNode.addRightEdge(self)
        rightNode.addLeftEdge(self)

    def __repr__(self) -> str:
        return self.letter

    def __eq__(self, value) -> bool:
        return self.letter == value
    
    def getRightNode(self) -> Node:
        return self.rightNode

    def getLetter(self) -> str:
        return self.letter


class Node:
    ID = 1
    def __init__(self, isTerminal: bool, isRoot: bool) -> None:
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.leftEdges: list[Edge] = []
        self.rightEdges: list[Edge] = []
        self.id = Node.ID
        Node.ID += 1

    def __repr__(self) -> str:
        return f"Node {self.id} connecting {self.leftEdges} to {self.rightEdges}"

    def addLeftEdge(self, edge: Edge) -> None:
        self.leftEdges.append(edge)

    def addRightEdge(self, edge: Edge) -> None:
        self.rightEdges.append(edge)

    def getLeftEdges(self) -> list[Edge]:
        return self.leftEdges
    
    def getRightEdges(self) -> list[Edge]:
        return self.rightEdges


class Trie:
    def __init__(self, rootNode: Node) -> None:
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
                lastNode = newNode

    def isTrieWord(self, word: str) -> bool:
        lastNode = self.rootNode
        for letter in word:
            rightEdges = lastNode.getRightEdges()
            if letter in rightEdges:
                index = rightEdges.index(letter)
                edge = rightEdges[index]
                lastNode = edge.getRightNode()
            else:
                return False
            

    
    


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load(filename: str):
    with open(filename, "rb") as f:
        return pickle.load(f)
    
if __name__ == "__main__":
    node1 = Node(False, True)
    node2 = Node(False, False)
    node3 = Node(True, True)
    edge1 = Edge("T", node1, node2)
    edge2 = Edge("O", node2, node3)
    print(node2)