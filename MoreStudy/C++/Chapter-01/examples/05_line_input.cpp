#include <iostream>
#include <string>

int main() {
    std::string full_name;

    std::cout << "Full name: ";
    std::getline(std::cin, full_name);
    std::cout << "Hello, " << full_name << "!\n";
    return 0;
}
