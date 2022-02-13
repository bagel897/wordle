#include "runner.h"
wordleRunner::wordleRunner(dictionary &dict, int size)
    : size(size), starting_dict(dict.con) {}
string wordleRunner::pickWord() {
  if(starting_dict.size() == 0) {
    cout << "ERROR no words" << endl;
    //TODO: error handling
  }
  int index = rand() % starting_dict.size();
  return *starting_dict.at(index);
}
string wordleRunner::guess(string givenWord, string guessedWord) {
  return make_guess(givenWord, guessedWord);
}
