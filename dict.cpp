#include "dict.h"
dictionary::dictionary(string filename, int length) {
  ifstream in(filename);
  string temp;
  while (in >> temp) {
    if (temp.length() == length) {
      transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
      con.push_back(new string(temp));
    }
  }
  this->length = length;
}
dictionary::~dictionary() {
  for (string *ptr : con) {
    delete (ptr);
  }
}
