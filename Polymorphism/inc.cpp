#define LI
#include <iostream>


class Vector{
public:
	#ifdef LIB
	Vector(){
		std::cout << "Using Library\n";
	}
	#else
	Vector(){
		std::cout << "Not using library\n";
	}
	#endif
};


int main() {
	Vector a;
    return 0;
}
