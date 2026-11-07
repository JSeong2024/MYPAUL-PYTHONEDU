#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: stream_state <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::println(stderr, "Open failed");
        return 1;
    }
    std::string line;
    std::size_t lines{};
    while (std::getline(input, line)) {
        ++lines;
    }
    if (input.bad()) {
        std::println(stderr, "Physical read error");
        return 1;
    }
    std::println("Lines: {}, EOF reached: {}", lines, input.eof());
}
