#include "solver.h"

wordleSolver::wordleSolver(dictionary &dict, int size)
    : current_dict(dict.con), size(size) {}
vector<vector<int>> wordleSolver::countByChar() {
  vector<vector<int>> counted(size, vector<int>(LETTERS, 0));
  for (string *word : current_dict) {
    for (int i = 0; i < size; i++) {
      counted.at(i).at(word->at(i) - 'a') += 1;
    }
  }
  return counted;
}
string wordleSolver::get_next_matrix() {
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
bool wordleSolver::checkWord(vector<char> required_chars, vector<int> counts,
                             vector<int> upper, string word) {
  char_array word_counts = {0};
  for (int i = 0; i < size; i++) {
    if ((required_chars.at(i) != ' ') && (word.at(i) != required_chars[i])) {
      return false;
    }
    word_counts.at(word.at(i) - 'a') += 1;
  }
  for (int i = 0; i < counts.size(); i++) {
    if ((counts.at(i) > word_counts.at(i)) ||
        (upper.at(i) < word_counts.at(i))) {
      return false;
    }
  }
  return true;
}
vector<string *> wordleSolver::filter(string user_input, string guessed_word) {
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
int wordleSolver::get_filter_size(string *first_word, string *second_word) {
  vector<string *> result =
      filter(make_guess(*first_word, *second_word), *first_word);
  int s = result.size();
  return s;
}
string wordleSolver::filter_next() {
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
  return *minWord;
}
string wordleSolver::get_next(string previous_guess, string user_input,
                              int algorithm) {
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
    return filter_next();
  }
}
