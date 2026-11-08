#include <iostream>
#include <string>
int main() {
    const std::string text{"한글"};
    std::cout << "UTF-8 bytes: " << text.size() << '\n';
}
