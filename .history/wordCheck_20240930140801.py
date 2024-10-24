import json
import itertools

def getWords() -> dict:
        dictionary = open("ENGLISH_DICTIONARY.txt").read().splitlines()
        wordsIncomplete = list(filter(lambda x: x.isupper(), dictionary))
        descriptions = []

        for i in range(len(dictionary)):
                if dictionary[i].isupper():
                        description = []
                        count = 1
                        while (not dictionary[i + count].isupper()) and (i + count != len(dictionary) - 1):
                                description.append(dictionary[i + count])
                                count += 1
                        descriptions.append("\n".join(description))

        words = {}
        for i in range(len(wordsIncomplete)):
                for w in wordsIncomplete[i].split("; "):
                  words[w.capitalize()] = descriptions[i]
                  
        return words

def getDefinitions() -> dict:
        dictionary: list[str] = open("ENGLISH_DICTIONARY.txt").read().splitlines()
        definitions: dict = {}
        for i in range(2, len(dictionary)):
                definition = ""
                index = i
                word = removeHyphen(dictionary[index - 2])
                if word.isupper() and (len(word) != 1) and (" " not in word) and ("." not in word):
                        definition = dictionary[index]
                        index += 1
                        while dictionary[index] or (not dictionary[index + 1].isupper() and dictionary[index + 1]):
                                definition += " " + dictionary[index]
                                index += 1
                if definition:
                        word = word
                        definitions[word.capitalize()] = definition
                i = index

        def mapping(x):
                if "Defn: " in x:
                        return " ".join(x.split("Defn: ")[1::])
                else:
                        return x

        for word in definitions:
                definition = definitions[word]
                definitionMapped = mapping(definition)
                definitions[word] = definitionMapped
        return definitions

def isWord(word: str) -> bool:
        with open("MyDictionary.json", "r") as f:
                words = json.load(f)
        if word.capitalize() in words:
                return True
        else:
                return False
        
def isPartialWord(part: str) -> bool:
        ...
        
def getDefinition(word: str) -> str:
        with open("MyDictionary.json", "r") as f:
                words = json.load(f)
        if not word.capitalize() in words:
                return "No such word exists."
        return words[word.capitalize()]

def removeHyphen(word: str) -> str:
        parts = word.split("-")
        wordNew = "".join(parts)
        return wordNew

def createMyDictionary() -> None:
        words = getDefinitions()
        print(dict(itertools.islice(words.items(), 10)))
        with open("/Users/MOPOLLIKA/Scrabble_NEA/MyDictionary.json", "w") as f:
                json.dump(words, f)

if __name__ == "__main__":
        print(getDefinition("eerie"))
        with open("MyDictionary.json", "r") as f:
                words = json.load(f)
                print(words)
                


        