import json

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
                word = dictionary[index - 2]
                if word.isupper():
                        definition = dictionary[index]
                        index += 1
                        while dictionary[index] or (not dictionary[index + 1].isupper() and dictionary[index + 1]):
                                definition += " " + dictionary[index]
                                index += 1
                if definition:
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
        word = word.capitalize()
        words = getDefinitions()
        if word in words and len(word) != 1:
                return True
        else:
                return False


if __name__ == "__main__":
        words = getDefinitions()
        words = {word: words[word] for word in words if len(word) != 1}
        
        with open("/Users/MOPOLLIKA/Scrabble_NEA/MyDictionary.json", "w") as f:
                json.dump(words, f)


        