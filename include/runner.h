#ifndef RUNNER
#define RUNNER
#include "dict.h"
#include "main.h"
class wordleRunner {
  int size;
  vector<string*>starting_dict;

public:
  wordleRunner(dictionary& dict, int size);
  string pickWord();
  string guess(string givenWord, string guessedWord);
};

#endif /* ! */
