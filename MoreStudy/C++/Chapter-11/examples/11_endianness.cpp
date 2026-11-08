#include <bit>
#include <iostream>
int main() {
    if (std::endian::native == std::endian::little) { std::cout << "Little endian\n"; }
    else if (std::endian::native == std::endian::big) { std::cout << "Big endian\n"; }
    else { std::cout << "Mixed endian\n"; }
}
