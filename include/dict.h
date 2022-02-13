#ifndef DICTIONARY_H
#define DICTIONARY_H
#include "main.h"
#include <fstream>
class dictionary {
public:
  vector<string *> con;
  int length;
  dictionary(string filename, int length);
  ~dictionary();
};
#endif
