#include <fstream>
#include <iostream>
#include <string>
int main(int argc,char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: count_lines <path>\n"; return 1; }
    std::ifstream input{argv[1]};
    if (!input) { return 1; }
    std::size_t count{};
    std::string line;
    while (std::getline(input,line)) { ++count; }
    if (input.bad()) { return 1; }
    std::cout << "Lines: " << count << '\n';
}
