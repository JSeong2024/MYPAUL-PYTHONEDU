#include <fstream>
#include <iostream>
#include <string>
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: read_lines <path>\n"; return 1; }
    std::ifstream input{argv[1]};
    if (!input) { std::cerr << "Cannot open file\n"; return 1; }
    std::string line;
    int count{};
    while (std::getline(input,line)) { ++count; std::cout << count << ": " << line << '\n'; }
    if (input.bad()) { std::cerr << "Read error\n"; return 1; }
}
