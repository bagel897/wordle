using namespace std;
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
import <iostream>;

const int LETTERS = 26;
class dictionary {
public:
  vector<string *> con;
  int length;
  dictionary(string filename, int length) {
    ifstream in;
    in.open(filename);
    string temp;
    while (in >> temp) {
      if (temp.length() == length) {
        transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
        con.push_back(new string(temp));
      }
    }
    this->length = length;
  }
  ~dictionary() {
    for (string *ptr : con) {
      delete (ptr);
    }
  }
};
int *count_chars(string *word) {
  int *result = new int[26];
  for (int i = 0; i < 26; i++) {
    result[i] = 0;
  }
  for (int i = 0; i < word->length(); i++) {
    result[word->at(i) - 'a'] += 1;
  }
  return result;
}
string make_guess(string given_word, string guessed_word) {
  int size = given_word.size();
  int *guessCounts = count_chars(&guessed_word);
  int *givenCounts = count_chars(&given_word);
  string result(size, 'B');
  for (int i = 0; i < size; i++) {
    if (given_word.at(i) == guessed_word.at(i)) {
      result[i] = 'G';
      givenCounts[given_word.at(i) - 'a'] -= 1;
    }
  }
  for (int i = 0; i < size; i++) {
    int ord = guessed_word[i] - 'a';
    if (guessCounts[ord] >= givenCounts[ord] && givenCounts[ord] != 0) {
      result[i] = 'Y';
      givenCounts[ord] -= 1;
    }
  }
  return result;
};
class wordleSolver {
  int size;
  dictionary *starting_dict;
  vector<string *> current_dict;
  map<string *, map<string *, vector<string *>>> precomputed;

public:
  wordleSolver(dictionary *dict, int size) {
    this->size = size;
    starting_dict = dict;
    reset();
  }
  void reset(bool precompute = false) {
    current_dict = starting_dict->con;
    if (precompute == true) {
      for (string *first : current_dict) {

        // precomputed.push_back(first);
        for (string *second : current_dict) {
        }
      }
    }
  }
  vector<vector<int>> countByChar() {
    vector<vector<int>> counted(size, vector<int>(LETTERS, 0));
    for (string *word : current_dict) {
      for (int i = 0; i < size; i++) {
        counted.at(i).at(word->at(i) - 'a') += 1;
      }
    }
    return counted;
  }
  string get_next_matrix() {
    vector<vector<int>> counted = countByChar();
    int currentScore;
    int maxScore = 0;
    string bestWord;
    for (string *word : current_dict) {
      currentScore = 0;
      for (int i = 0; i < size; i++) {
        currentScore += counted.at(i).at(word->at(i) - 'a');
      }
      if (currentScore > maxScore) {
        maxScore = currentScore;
        bestWord = *word;
      }
    }
    return bestWord;
  }
  bool checkWord(vector<char> required_chars, vector<int> counts,
                 vector<int> upper, string word) {
    int word_counts[26] = {0};
    for (int i = 0; i < size; i++) {
      if ((required_chars.at(i) != ' ') && (word.at(i) != required_chars[i])) {
        return false;
      }
      word_counts[word.at(i) - 'a'] += 1;
    }
    for (int i = 0; i < counts.size(); i++) {
      if ((counts.at(i) > word_counts[i]) || (upper.at(i) < word_counts[i])) {
        return false;
      }
    }
    return true;
  }
  vector<string *> filter(string user_input, string guessed_word) {
    vector<string *> filtered_dictionary;
    vector<char> requiredChars(LETTERS, ' ');
    vector<int> counts_lower(LETTERS, 0);
    vector<int> counts_upper(LETTERS, size);
    for (int i = 0; i < size; i++) {
      if (user_input.at(i) == 'B') {
        counts_upper.at(guessed_word.at(i) - 'a') = 0;
      }
    }
    int ord;
    for (int i = 0; i < size; i++) {
      switch (user_input[i]) {
      case 'G':
        requiredChars.at(i) = guessed_word.at(i);
      case 'Y':
        ord = guessed_word.at(i) - 'a';
        counts_upper.at(ord) += 1;
        counts_lower.at(ord) += 1;
        break;
      default:
        break;
      }
    }
    for (string *word : current_dict) {
      if (checkWord(requiredChars, counts_lower, counts_upper, *word)) {
        filtered_dictionary.push_back(word);
      }
    }
    return filtered_dictionary;
  }
  int get_filter_size(string *first_word, string *second_word) {
    vector<string *> result =
        filter(make_guess(*first_word, *second_word), *first_word);
    int s = result.size();
    return s;
  }
  string *filter_next() {
    float minscore = 100;
    int current_size;
    float score;
    string *minWord;
    for (string *first_word : current_dict) {
      current_size = 0;
      for (string *second_word : current_dict) {
        current_size += get_filter_size(first_word, second_word);
      }
      score = abs(current_size - current_dict.size() / 2.0);
      if (score < minscore) {
        minscore = score;
        minWord = first_word;
      }
    }
    return minWord;
  }
  string get_next(string previous_guess, string user_input, int algorithm) {
    if (user_input.length() != 0) {
      current_dict = filter(user_input, previous_guess);
    }
    if (current_dict.size() == 0) {
      return "";
    }
    if (current_dict.size() == 1) {
      return *current_dict.at(0);
    }
    if (algorithm == 0) {
      return get_next_matrix();
    } else {
      return *filter_next();
    }
  }
};

class wordleRunner {
  int size;
  dictionary *starting_dict;

public:
  wordleRunner(dictionary *dict, int size) {
    this->size = size;
    starting_dict = dict;
  }
  string pickWord() {
    int index = rand() % starting_dict->con.size();
    return *starting_dict->con.at(index);
  }
  string guess(string givenWord, string guessedWord) {
    return make_guess(givenWord, guessedWord);
  }
};
int run_round(wordleSolver solver, wordleRunner game, int size, int algorithm) {
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
  wordleSolver solver(&dict, size);
  wordleRunner runner(&dict, size);
  vector<int> results;
  for (int i = 0; i < count; i++) {
    results.push_back(run_round(solver, runner, size, 1));
    solver.reset();
    cout << results.at(i) << "\t";
  }
  cout << endl;
}
int main() { runGame(5, 10); }
