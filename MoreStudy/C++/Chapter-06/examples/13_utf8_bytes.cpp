#include <climits>
#include <iostream>
#include <string>

int main() {
    const std::string ascii{"ABC"};
    const std::string korean{"가"}; // UTF-8 소스 및 실행 문자 인코딩 가정
    std::cout << "Bits per byte: " << CHAR_BIT << '\n';
    std::cout << "ASCII bytes: " << ascii.size() << '\n';
    std::cout << "Korean bytes (UTF-8): " << korean.size() << '\n';
}
