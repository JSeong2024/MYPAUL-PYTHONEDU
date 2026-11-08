#include <iostream>

int square(int number) {
    return number * number;
}

void print_result(int value) {
    std::cout << "Squared: " << value << '\n';
}

int main() {
    const int answer{square(6)};
    print_result(answer);
}
