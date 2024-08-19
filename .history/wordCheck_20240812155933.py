def getWords():
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

def getDefinitions():
        

def isWord(word):
        word = word.capitalize()
        words = getWords()
        if word in words:
                return True, words[word]
        else:
                return False, None


if __name__ == "__main__":
        print(isWord("pet"))


        