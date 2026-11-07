#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: read_lines <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::println(stderr, "Cannot open file");
        return 1;
    }
    std::string line;
    std::size_t count{};
    while (std::getline(input, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        ++count;
        std::println("{}: {}", count, line);
    }
    if (input.bad()) {
        std::println(stderr, "Read error");
        return 1;
    }
    std::println("Lines: {}", count);
}
