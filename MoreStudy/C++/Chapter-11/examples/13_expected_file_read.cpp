#include <fstream>
#include <iostream>
#include <optional>
#include <string>
std::optional<std::string> first_line(const std::string& path) {
    std::ifstream input{path};
    std::string line;
    if (!input || !std::getline(input,line)) { return std::nullopt; }
    return line;
}
int main(int argc, char* argv[]) {
    if (argc != 2) { std::cerr << "Usage: first_line <path>\n"; return 1; }
    const auto line = first_line(argv[1]);
    if (!line) { std::cerr << "No first line\n"; return 1; }
    std::cout << "First line: " << *line << '\n';
}
