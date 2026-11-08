#include <fstream>
#include <iostream>
#include <string>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: read_text_file <path>\n"; return 1; }
    std::ifstream input{argv[1], std::ios::binary};
    if (!input) { std::cerr << "Cannot open file\n"; return 1; }
    std::string content;
    char character{};
    while (input.get(character)) { content.push_back(character); }
    if (input.bad()) { std::cerr << "Read error\n"; return 1; }
    std::cout << "Bytes: " << content.size() << '\n';
}
