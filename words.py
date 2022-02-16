from __future__ import annotations

import random
import string
import time
from typing import List, Tuple

a_ord: int = ord("a")


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
    guess_counts: List[bool] = [False for _ in string.ascii_lowercase]
    given_counts: List[bool] = [False for _ in string.ascii_lowercase]
    result = ["B" for _ in range(size)]
    for i in range(size):
        guess_counts[ord(guessedWord[i]) - a_ord] = True
        given_counts[ord(givenWord[i]) - a_ord] = True
    for i in range(size):
        gord: int = ord(guessedWord[i]) - a_ord
        if guess_counts[gord] and given_counts[gord]:
            result[i] = "Y"
    for i in range(size):
        if givenWord[i] == guessedWord[i]:
            result[i] = "G"
    return arrayToStr(result)


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
    counted: List[List[int]]

    def __init__(self, size: int):
        self.dictionary = getDict(size)
        self.size = size

    def countByChar(self, wordList: List[str]) -> None:
        self.counted: List[List[int]] = [
            [0 for _ in string.ascii_lowercase] for _ in range(self.size)
        ]
        for word in wordList:
            for i in range(self.size):
                self.counted[i][ord(word[i]) - a_ord] += 1

    def get_score_matrix_word(self, word: str) -> int:
        score: int = 0
        for i in range(self.size):
            score += self.counted[i][ord(word[i]) - a_ord]
        return score

    def get_next_matrix(self, dictionary: List[str]) -> str:
        return max(dictionary, key=(self.get_score_matrix_word))

    def checkWord(
        self,
        requiredChars: List[str],
        has_char: List[bool],
        no_char: List[bool],
        word: str,
        bannedChars: List[str],
    ) -> bool:
        word_counts: List[bool] = [False for _ in string.ascii_lowercase]
        for i in range(self.size):
            if requiredChars[i] != "" and word[i] != requiredChars[i]:
                return False
            if bannedChars[i] != "" and word[i] == bannedChars[i]:
                return False
            word_counts[ord(word[i]) - a_ord] = True
        for i in range(26):
            if has_char[i] and not word_counts[i]:
                return False
            if not no_char[i] and word_counts[i]:
                return False
        return True

    def filter(
        self, dictionary: List[str], userInput: str, guessedWord: str
    ) -> List[str]:
        requiredChars: List[str] = ["" for i in range(self.size)]
        bannedChars: List[str] = ["" for i in range(self.size)]
        has_char: List[bool] = [False for _ in string.ascii_lowercase]
        has_upper: List[bool] = [True for _ in string.ascii_lowercase]
        for i in range(self.size):
            if userInput[i] == "B":
                has_upper[ord(guessedWord[i]) - a_ord] = False
        for i in range(self.size):
            if userInput[i] == "G":
                requiredChars[i] = guessedWord[i]
                has_char[ord(guessedWord[i]) - a_ord] = True
                has_upper[ord(guessedWord[i]) - a_ord] = True
            elif userInput[i] == "Y":
                bannedChars[i] = guessedWord[i]
                has_char[ord(guessedWord[i]) - a_ord] = True
        return [
            word
            for word in dictionary
            if self.checkWord(requiredChars, has_char, has_upper, word, bannedChars)
        ]

    # def filter_next(self, dictionary: List[str]) -> str:
    #     results = {}
    #     for try_guess in dictionary:
    #         size = 0
    #         for real_word in dictionary:
    #             size += len(
    #                 self.filter(
    #                     dictionary, guess(self.size, try_guess, real_word), real_word
    #                 )
    #             )
    #         results[guess] = abs(size - len(dictionary) * 1 / 2)
    #     return min(results, key=results.get)

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
            self.countByChar(dictionary)
            guess = self.get_next_matrix(dictionary)
        # else:
        #     guess = self.filter_next(dictionary)
        return (guess, dictionary)


def runRound(
    solver: wordSolver, game: wordle, size: int, algorithm: int, userInput: bool = False
) -> int:
    game.pickWord()
    guesses: List[str] = []
    results: List[str] = []
    dictionary = solver.dictionary
    result: str = ""
    guess: str = arrayToStr(["a" for _ in range(size)])
    success: str = arrayToStr(["G" for _ in range(size)])
    count = 0
    while True:
        guess, dictionary = solver.get_next(dictionary, guess, result, algorithm)
        if guess == "":
            print(guesses)
            print(results)
            print(game.word)
            return 100
        if userInput:
            print(guess)
            result = input()
        else:
            guesses.append(guess)
            result = game.guess(game.word, guess)
            results.append(result)
        count += 1
        if result == success:
            return count
        if count > 10:
            return 101


def runGame(size: int, count: int, userInput: bool = False):
    solver = wordSolver(size)
    game = wordle(size)
    results = []
    start: float = time.time()
    for _ in range(count):
        results.append(runRound(solver, game, size, 0, userInput))
    stop: float = time.time()
    print(f"average guess:{sum(results)/count}, time per guess {(stop-start)/count}")


if __name__ == "__main__":
    runGame(5, 1000, False)
