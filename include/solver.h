#ifndef SOLVER
#define SOLVER
#include "dict.h"
#include <map>
class wordleSolver {
  int size;
  vector<string *> current_dict;
  map<string *, map<string *, vector<string *>>> precomputed;

public:
  wordleSolver(dictionary &dict, int size);
  vector<vector<int>> countByChar();
  string get_next_matrix();
  bool checkWord(vector<char> required_chars, vector<int> counts,
                 vector<int> upper, string word);
  vector<string *> filter(string user_input, string guessed_word);
  int get_filter_size(string *first_word, string *second_word);
  string filter_next();
  string get_next(string previous_guess, string user_input, int algorithm);
};

#endif
