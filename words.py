from typing import List, Dict
import string

a_ord = ord("a")


class wordSolver:
    dictionary: List[str]
    size: int

    def __init__(self, size: int):
        dictionary = "words.txt"
        self.dictionary = []
        with open(dictionary) as f:
            for word in f:
                wordLen = len(word) - 1
                if wordLen == size:
                    self.dictionary.append(word[:wordLen].lower())
        self.size = size

    def countByChar(self, wordList: List[str]) -> List[List[int]]:
        counted: List[List[int]] = [
            [0 for _ in string.ascii_lowercase] for _ in range(self.size)
        ]
        for word in wordList:
            for i in range(self.size):
                counted[i][ord(word[i]) - a_ord] += 1
        return counted

    def getNextWord(self, counted: List[List[int]], dictionary: List[str]):
        scores: Dict[str, int] = {}
        for word in dictionary:
            score: int = 0
            for i in range(self.size):
                score += counted[i][ord(word[i]) - a_ord]
            scores[word] = score
        return max(scores, key=scores.get)

    def checkWord(
        self,
        requiredChars: List[str],
        counts: List[int],
        upper: List[int],
        word: str,
    ) -> bool:
        word_counts: List[int] = [0 for _ in string.ascii_lowercase]
        for i in range(self.size):
            if requiredChars[i] != "" and word[i] != requiredChars[i]:
                return False
            word_counts[ord(word[i]) - a_ord] += 1
        for i in range(len(counts)):
            if counts[i] > word_counts[i]:
                return False
            if upper[i] < word_counts[i]:
                return False
        return True

    def filter(
        self, dictionary: List[str], userInput: str, guessedWord: str
    ) -> List[str]:
        newDict: List[str] = []
        requiredChars: List[str] = ["" for i in range(self.size)]
        counts_lower: List[int] = [0 for _ in string.ascii_lowercase]
        counts_upper: List[int] = [self.size for _ in string.ascii_lowercase]
        for i in range(self.size):
            if userInput[i] == "B":
                counts_upper[ord(guessedWord[i]) - a_ord] = 0
        for i in range(self.size):
            if userInput[i] == "G":
                requiredChars[i] = guessedWord[i]
                counts_lower[ord(guessedWord[i]) - a_ord] += 1
                counts_upper[ord(guessedWord[i]) - a_ord] += 1
            elif userInput[i] == "Y":
                counts_upper[ord(guessedWord[i]) - a_ord] += 1
                counts_lower[ord(guessedWord[i]) - a_ord] += 1
        for word in dictionary:
            if self.checkWord(requiredChars, counts_lower, counts_upper, word):
                newDict.append(word)
        return newDict

    def runTurn(self, dictionary: List[str], guess: str):
        userInput = input()
        if userInput == "q":
            return ""
        if len(userInput) == self.size:
            dictionary = self.filter(dictionary, userInput, guess)
            if len(dictionary) == 1:
                print(f"the only word is {dictionary[0]} Good Job")
                return ""
            counted = self.countByChar(dictionary)
            guess = self.getNextWord(counted, dictionary)
            print(guess)
            self.runTurn(dictionary, guess)
        else:
            print("invalid input")

    def runGame(self):
        # start
        dictionary = self.dictionary
        counted = self.countByChar(dictionary)
        guess = self.getNextWord(counted, dictionary)
        print(guess)
        self.runTurn(dictionary, guess)


if __name__ == "__main__":
    solver = wordSolver(5)
    solver.runGame()
