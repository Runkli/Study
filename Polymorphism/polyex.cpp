#include <iostream>
using std::cin;
using std::cout;
using std::endl;

#include <vector>
using std::vector;

#include <functional>
using std::function;

class lib {
public:
    lib() {};
    function< int() > give{ [] () { return 0; } };
  //  lib( const lib& l ) { give = l.give; };
};

class lib1 : public lib {
public:
    lib1() : lib() { give = [] () { return 1; }; };
};

class lib2 : public lib {
public:
    lib2() : lib() { give = [] () { return 2; }; };
};

int main() {

    // we can invoke the specific library
    lib2 specific;
    cout << specific.give() << endl;

    // if we use the copy contructor we also get the `derived' funciton
    lib mylib( specific );
    cout << mylib.give() << endl;

    return 0;
}
