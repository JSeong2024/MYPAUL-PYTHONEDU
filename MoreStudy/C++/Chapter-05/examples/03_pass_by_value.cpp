#include <iostream>
#include <string>

std::string add_suffix(std::string name) {
    name += "-A";
    return name;
}

int main() {
    const std::string original{"SENSOR"};
    std::cout << "Original: " << original << '\n';
    std::cout << "Updated: " << add_suffix(original) << '\n';
}
