#ifndef MAIN_H
#define MAIN_H
#include <algorithm>
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;
const int LETTERS = 26;
typedef array<int, LETTERS> char_array;
string make_guess(string given_word, string guessed_word);
#endif // !
