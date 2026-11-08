#include <iostream>
#include <sstream>
#include <string>
int main() {
    std::istringstream source{"12 abc"};
    int number{};
    source >> number;
    std::cout << "First: " << number << '\n';
    source >> number;
    std::cout << std::boolalpha << "Failed: " << source.fail() << '\n';
    source.clear();
    std::string invalid;
    source >> invalid;
    std::cout << "Token: " << invalid << '\n';
}
