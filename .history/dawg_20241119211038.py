import pickle
import json
import time
from itertools import permutations, combinations
from typing import Callable

LETTERS_SCORES: dict = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, 
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, 
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "BLANK": 0}
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
FILENAME = "trie.pkl"

def timeLog(func: Callable) -> Callable:
    def wrapper(*args):
        timeStart = time.time()

        result = func(*args)

        timeEnd = time.time()
        print(f"Time taken for function `{func.__name__}` to execute: {timeEnd - timeStart}s")
        return result

    return wrapper

def listToStr(lst: list) -> str:
    result: str = ""
    for letter in lst:
        result += letter
    return result

def rawScore(word: str) -> int:
    score = 0
    for letter in word:
        score += LETTERS_SCORES[letter.upper()]
    return score

def searchMaxScore(words: list[str]) -> tuple[int, int]:
    scores = list(map(lambda x: rawScore(x), words))
    score = max(scores)
    scoreIndex = scores.index(score)
    return score, scoreIndex

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
    
    def getLeftNode(self):
        return self.leftNode
    
    def getRightNode(self):
        return self.rightNode

    def getLetter(self) -> str:
        return self.letter


class Node:
    ID = 1
    def __init__(self, isTerminal: bool, isRoot: bool) -> None:
        self.isTerminal = isTerminal
        self.isRoot = isRoot
        self.isSearched = False
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

    def setTerminal(self) -> None:
        self.isTerminal = True

    def setSearched(self) -> None:
        self.isSearched = True

    def getLeftEdges(self) -> list[Edge]:
        return self.leftEdges
    
    def getRightEdges(self) -> list[Edge]:
        return self.rightEdges
    
    def getIsTerminal(self) -> bool:
        return self.isTerminal
    
    def getIsSearched(self) -> bool:
        return self.isSearched

class Trie:
    def __init__(self) -> None:
        self.rootNode = Node(isTerminal=False, isRoot=True)
    
    def assemble(self, vocabulary: dict[str, str]) -> None:
        lastNode = self.rootNode
        isRoot = True
        # Going through each word in the alphabet
        for word in vocabulary.keys():
            lettersUsed = ""
            firstLetter = word[0]
            rightEdges = lastNode.getRightEdges()
            rightEdgesAvailable = [edge for edge in rightEdges if edge == firstLetter]
            if rightEdgesAvailable != []:
                edge = rightEdgesAvailable[0]
                lastNode= edge.getRightNode()
                wordRemainder = word[1::]
            else:
                wordRemainder = word

            for letter in wordRemainder:
                lettersUsed += letter
                isTerminal = (lettersUsed == word)

                newNode = Node(isTerminal, isRoot)
                newEdge = Edge(letter, lastNode, newNode)
                lastNode = newNode
            lastNode.setTerminal()

            lastNode = self.rootNode

    def _searchRightRecursively(self, node: Node, word: str, depth: int) -> bool:
        rightEdges = node.getRightEdges()
        letter = word[depth]
        rightEdgesAvailable = list(filter(lambda x: x == letter and not x.getRightNode().getIsSearched(), rightEdges))
        # Stopping criterion
        if depth == len(word) - 1 and node.getIsTerminal():
            return True
        # Going back if no letter is found and set the current node isSearched flag true
        if len(rightEdgesAvailable) == 0:
            depth -= 1
            # No such word found and the depth went behind the root node
            if depth == -1:
                return False
            previousNode = node.getLeftEdges()[0].getLeftNode()
            node.setSearched()
            return self._searchRight(previousNode, word, depth)

        edge = rightEdgesAvailable[0]
        nextNode = edge.getRightNode()
        print(nextNode)
        return self._searchRight(nextNode, word, depth + 1)
    
    def dfs(self, node: Node, currentWord: str, wordSearched: str) -> bool | None:
        print(f"Current node: {node}, current word: {currentWord}")
        if currentWord == wordSearched and node.getIsTerminal():
            return True
        letter = wordSearched[len(currentWord)]
        rightEdges = node.getRightEdges()
        rightEdgesAvailable = list(filter(lambda x: x == letter, rightEdges))
        for edge in rightEdgesAvailable:
            nextNode = edge.getRightNode()
            return self.dfs(nextNode, currentWord + letter, wordSearched)

    def bashSearch(self, word: str) -> bool:
        word = word.capitalize()
        node = self.rootNode
        rightEdges = node.getRightEdges()
        rightEdgesAvailable = list(filter(lambda x: x == word[0], rightEdges))
        for edge in rightEdgesAvailable:
            node = edge.getRightNode()
            wordTail = self._goRight(node, "")
            if word[0] + wordTail == word:
                return True
        return False

    def _goRight(self, node: Node, currentWord: str) -> str:
        if node.getIsTerminal():
            return currentWord
        nextEdge = node.getRightEdges()[0]
        nextNode = nextEdge.getRightNode()
        currentWord += nextEdge.getLetter()
        return self._goRight(nextNode, currentWord)
        

    def isTrieWord(self, word: str) -> bool:
        startNode = self.rootNode
        depth = 0
        return self._searchRight(startNode, word, depth)
    
    def generateOptimalWord(self, letters: str, difficulty: int = 6):
        """This method finds all the possible words that can be assembled from the rack letters.
        These words are arranged in the descending score order.
        Let's try bashing it."""
        possibleWords = []
        # go through all lengths of words, starting from 2
        for length in range(2, len(letters) + 1):
            # go through all the `length` size combinations of letters
            for combination in combinations(letters, length):
                possible = self._searchConstantLengthWords(combination)
                if not possible:
                    continue
                maxScore, maxScoreIndex = searchMaxScore(possible)
                optimalWord = possible[maxScoreIndex]
                if maxScore >= difficulty and optimalWord not in possibleWords:
                    yield optimalWord
                possibleWords += possible
        return None
    
    def _searchConstantLengthWords(self, letters: str) -> list[str]:
        words = list(permutations(letters))
        possible = []
        for word in words:
            word = listToStr(word)
            if self.bashSearch(word):
                possible.append(word)
        return possible
        

class Dawg(Trie):
    def __init__(self, rootNode):
        super().__init__(rootNode)

    def _assemble(self, vocabulary: dict[str, str]) -> None:
        super()._assemble(vocabulary)


def save(object: object, filename: str):
    with open(filename, "wb") as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

def load(filename: str):
    with open(filename, "rb") as f:
        obj = pickle.load(f)
        f.close()
        return obj
    
if __name__ == "__main__":
    """
    node1 = Node(False, True)
    node2 = Node(False, False)
    node3 = Node(True, True)
    edge1 = Edge("T", node1, node2)
    edge2 = Edge("O", node2, node3)
    """
    
    with open("MyDictionary.json", "r") as f:
        words = json.load(f)
        f.close()

    trie = Trie()
    trie.assemble(words)
    t1 = time.time()
    gen = trie.generateOptimalWord(["A", "C", "I", "D", "M", "U", "M"])
    for i in gen:
        print(i)
    print(time.time() - t1)


    