#include <iostream>
#include <print>
#include <string>

int main() {
    using std::println;
    using std::string;

    string name;
    if (!std::getline(std::cin, name) ||
        name.find_first_not_of(" \t\r") == string::npos) {
        std::cerr << "Error: name is required.\n";
        return 1;
    }

    println("Hello, {}!", name);
    return 0;
}
