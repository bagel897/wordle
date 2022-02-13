from __future__ import annotations
from typing import List, Dict, Tuple
import string
import random

a_ord = ord("a")


def arrayToStr(input: List[str]) -> str:
    result = ""
    for char in input:
        result += char
    return result


def getDict(size: int) -> List[str]:
    dictionary_file = "words.txt"
    dictionary = []
    with open(dictionary_file) as f:
        for word in f:
            wordLen = len(word) - 1
            if wordLen == size:
                dictionary.append(word[:wordLen].lower())
    return dictionary


def guess(size, givenWord: str, guessedWord: str) -> str:
    guess_counts: List[int] = [0 for _ in string.ascii_lowercase]
    given_counts: List[int] = [0 for _ in string.ascii_lowercase]
    result = ["B" for _ in range(size)]
    for i in range(size):
        guess_counts[ord(guessedWord[i]) - a_ord] += 1
        given_counts[ord(givenWord[i]) - a_ord] += 1
    for i in range(size):
        if givenWord[i] == guessedWord[i]:
            result[i] = "G"
            given_counts[ord(givenWord[i]) - a_ord] -= 1
    for i in range(size):
        gord: int = ord(guessedWord[i]) - a_ord
        if guess_counts[gord] >= given_counts[gord] and given_counts[gord] != 0:
            result[i] = "Y"
            given_counts[gord] -= 1
    result_str: str = ""
    for char in result:
        result_str += char
    return result_str


class wordle:
    dictionary: List[str]
    size: int
    word: str

    def __init__(self, size: int):
        self.dictionary = getDict(size)
        self.size = size

    def pickWord(self):
        self.word = self.dictionary[random.randint(0, len(self.dictionary))]

    def guess(self, givenWord: str, guessedWord: str) -> str:
        return guess(self.size, givenWord, guessedWord)


class wordSolver:
    dictionary: List[str]
    size: int

    def __init__(self, size: int):
        self.dictionary = getDict(size)
        self.size = size

    def countByChar(self, wordList: List[str]) -> List[List[int]]:
        counted: List[List[int]] = [
            [0 for _ in string.ascii_lowercase] for _ in range(self.size)
        ]
        for word in wordList:
            for i in range(self.size):
                counted[i][ord(word[i]) - a_ord] += 1
        return counted

    def get_next_matrix(self, counted: List[List[int]], dictionary: List[str]) -> str:
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

    def filter_next(self, dictionary: List[str]) -> str:
        results = {}
        for try_guess in dictionary:
            size = 0
            for real_word in dictionary:
                size += len(
                    self.filter(
                        dictionary, guess(self.size, try_guess, real_word), real_word
                    )
                )
            results[guess] = abs(size - len(dictionary) * 1 / 2)
        return min(results, key=results.get)

    def get_next(
        self, dictionary: List[str], prev_guess: str, userInput: str, algorithm: int
    ) -> Tuple[str, List[str]]:
        if not userInput == "":
            dictionary = self.filter(dictionary, userInput, prev_guess)
        if len(dictionary) == 1:
            return (dictionary[0], dictionary)
        if len(dictionary) == 0:
            return ("", dictionary)
        if algorithm == 0:
            counted = self.countByChar(dictionary)
            guess = self.get_next_matrix(counted, dictionary)
        else:
            guess = self.filter_next(dictionary)
        return (guess, dictionary)


def runRound(solver: wordSolver, game: wordle, size: int, algorithm: int, userInput: bool = False) -> int:
    game.pickWord()
    dictionary = solver.dictionary
    result: str = ""
    guess: str = arrayToStr(["a" for _ in range(size)])
    success: str = arrayToStr(["G" for _ in range(size)])

    count = 0
    while True:
        guess, dictionary = solver.get_next(dictionary, guess, result, algorithm)
        if guess == "":
            return 100
        if userInput:
            print(guess)
            result = input()
        else:
            result = game.guess(game.word, guess)
        count += 1
        if result == success:
            return count
        if count > 10:
            return 101


def runGame(size: int, count: int, userInput: bool = False):
    solver = wordSolver(size)
    game = wordle(size)
    results = []
    for _ in range(count):
        results.append(runRound(solver, game, size, 0, userInput))
    print(results)


if __name__ == "__main__":
     runGame(5, 10, True)
    
