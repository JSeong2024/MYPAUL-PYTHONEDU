#include <iostream>
#include <string>

int main() {
    std::string name;

    std::cout << "Full name: ";
    std::getline(std::cin, name);
    std::cout << "Welcome, " << name << "!\n";
    return 0;
}
