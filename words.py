

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


def guess(size: int, givenWord: str, guessedWord: str) -> str:
    guess_counts: List[int] = [0 for _ in string.ascii_lowercase]
    given_counts: List[int] = [0 for _ in string.ascii_lowercase]
    result = ["B" for _ in range(size)]
    for i in range(size):
        guess_counts[ord(guessedWord[i]) - a_ord] += 1
        given_counts[ord(givenWord[i]) - a_ord] += 1
    for i in range(size):
        if givenWord[i] == guessedWord[i]:
            result[i] = "G"
            given_counts[ord(guessedWord[i]) - a_ord] -= 1

    for i in range(size):
        gord: int = ord(guessedWord[i]) - a_ord
        if guess_counts[gord] > 0 and given_counts[gord] > 0 and result[i] == "B":
            result[i] = "Y"
            given_counts[gord] -= 1
    return arrayToStr(result)


class guess_objext:
    def __init__(self, userInput: str, guessedWord: str, size: int):
        self.size = size
        self.requiredChars: List[str] = ["" for i in range(self.size)]
        self.bannedChars: List[str] = ["" for i in range(self.size)]
        self.has_char: List[int] = [0 for _ in string.ascii_lowercase]
        self.has_upper: List[int] = [self.size for _ in string.ascii_lowercase]
        for i in range(self.size):
            if userInput[i] == "B":
                self.has_upper[ord(guessedWord[i]) - a_ord] = 0
        for i in range(self.size):
            if userInput[i] == "G":
                self.requiredChars[i] = guessedWord[i]
                self.has_char[ord(guessedWord[i]) - a_ord] += 1
                self.has_upper[ord(guessedWord[i]) - a_ord] += 1
            elif userInput[i] == "Y":
                self.bannedChars[i] = guessedWord[i]
                self.has_char[ord(guessedWord[i]) - a_ord] += 1
                self.has_upper[ord(guessedWord[i]) - a_ord] += 1

    def checkWord(self, word: str) -> bool:
        word_counts: List[int] = [0 for _ in string.ascii_lowercase]
        for i in range(self.size):
            if self.requiredChars[i] != "" and word[i] != self.requiredChars[i]:
                return False
            if self.bannedChars[i] != "" and word[i] == self.bannedChars[i]:
                return False
            word_counts[ord(word[i]) - a_ord] += 1
        for i in range(26):
            if self.has_char[i] > word_counts[i]:
                return False
            if self.has_upper[i] < word_counts[i]:
                return False
        return True


class wordle:
    dictionary: List[str]
    size: int
    word: str

    def __init__(self, size: int):
        self.dictionary = getDict(size)
        self.size = size

    def pickWord(self) -> None:
        self.word = self.dictionary[random.randint(0, len(self.dictionary) - 1)]

    def guess(self, givenWord: str, guessedWord: str) -> str:
        return guess(self.size, givenWord, guessedWord)


class wordSolver:
    dictionary: List[str]
    size: int
    counted: List[List[int]]
    on_letter: int

    def __init__(self, size: int, on_letter: int):
        self.dictionary = getDict(size)
        self.size = size
        self.on_letter = on_letter

    def countByChar(self, wordList: List[str]) -> None:
        self.counted: List[List[int]] = [
            [0 for _ in string.ascii_lowercase] for _ in range(self.size)
        ]
        other_letter = 1
        for word in wordList:
            for i in range(self.size):
                self.counted[i][ord(word[i]) - a_ord] += self.on_letter
                for j in range(self.size):
                    self.counted[j][ord(word[i]) - a_ord] += other_letter

    def get_score_matrix_word(self, word: str) -> int:
        score: int = 0
        for i in range(self.size):
            score += self.counted[i][ord(word[i]) - a_ord]
        return score

    def get_next_matrix(self, dictionary: List[str]) -> str:
        return max(dictionary, key=(self.get_score_matrix_word))

    def filter(
        self, dictionary: List[str], userInput: str, guessedWord: str
    ) -> List[str]:
        guess = guess_objext(userInput, guessedWord, self.size)
        return [word for word in dictionary if guess.checkWord(word)]

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


def runGame(size: int, count: int, userInput: bool, on_letter: int) -> float:
    solver = wordSolver(size, on_letter)
    game = wordle(size)
    results = []
    start: float = time.time()
    for _ in range(count):
        results.append(runRound(solver, game, size, 0, userInput))
    stop: float = time.time()
    print(f"average guess:{sum(results)/count}, time per guess {(stop-start)/count}")
    return sum(results) / count


def on_letter_test() -> None:
    for i in range(20):
        runGame(5, 1000, False, i)


if __name__ == "__main__":
    # runGame(5, 1000, False)
    on_letter_test()
