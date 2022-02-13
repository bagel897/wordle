#include "runner.h"
#include "solver.h"

char_array count_chars(string *word) {
  char_array result = {0};
  for (char c : *word) {
    result.at(c - 'a') += 1;
  }
  return result;
}
string make_guess(string given_word, string guessed_word) {
  int size = given_word.size();
  char_array guessCounts = count_chars(&guessed_word);
  char_array givenCounts = count_chars(&given_word);
  string result(size, 'B');
  for (int i = 0; i < size; i++) {
    if (given_word.at(i) == guessed_word.at(i)) {
      result[i] = 'G';
      givenCounts.at(given_word.at(i) - 'a') -= 1;
    }
  }
  for (int i = 0; i < size; i++) {
    int ord = guessed_word[i] - 'a';
    if (guessCounts.at(ord) >= givenCounts.at(ord) &&
        givenCounts.at(ord) != 0) {
      result[i] = 'Y';
      givenCounts.at(ord) -= 1;
    }
  }
  return result;
};

int run_round(dictionary &dict, int size, int algorithm) {
  wordleSolver solver(dict, size);
  wordleRunner game(dict, size);
  string correct = game.pickWord();
  string result = "";
  string guess = "";
  string success(size, 'G');
  for (int count = 1; count < 10; count++) {
    guess = solver.get_next(guess, result, algorithm);
    if (guess.length() == 0) {
      return 100;
    }
    result = game.guess(correct, guess);
    if (result == success) {
      return count;
    }
  }
  return 101;
}
void runGame(int size, int count) {
  dictionary dict("words.txt", size);
  vector<int> results;
  for (int i = 0; i < count; i++) {
    results.push_back(run_round(dict, size, 0));
    cout << results.at(i) << endl;
  }
  cout << endl;
}
int main() {
  srand(time(0));
  runGame(5, 10);
}
