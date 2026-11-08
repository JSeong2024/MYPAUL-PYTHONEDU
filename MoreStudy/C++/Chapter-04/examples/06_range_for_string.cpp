#include <iostream>
#include <string>

int main() {
    const std::string code{"A1B2C"};
    int digit_count{};

    for (const char character : code) {
        if (character >= '0' && character <= '9') {
            ++digit_count;
        }
    }

    std::cout << "Code: " << code << '\n';
    std::cout << "Digits: " << digit_count << '\n';
}
