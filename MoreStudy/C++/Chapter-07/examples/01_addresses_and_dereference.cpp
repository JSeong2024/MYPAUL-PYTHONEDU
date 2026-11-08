#include <iostream>

int main() {
    int temperature{24};
    int* reading{&temperature};
    std::cout << "Original: " << temperature << " C\n";
    *reading = 26;
    std::cout << "Updated: " << temperature << " C\n";
    std::cout << std::boolalpha;
    std::cout << "Same object: " << (reading == &temperature) << '\n';
}
