#include <iostream>
#include <string>

int main() {
    std::string name;
    std::string interest;

    std::cout << "Name: ";
    std::getline(std::cin, name);
    std::cout << "Interest: ";
    std::getline(std::cin, interest);

    std::cout << "Profile: " << name << " | " << interest << '\n';
    return 0;
}
