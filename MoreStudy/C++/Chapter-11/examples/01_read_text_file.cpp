#include <fstream>
#include <iterator>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::println(stderr, "Usage: read_text_file <path>");
        return 1;
    }
    std::ifstream input{argv[1]};
    if (!input) {
        std::println(stderr, "Cannot open input file");
        return 1;
    }
    const std::string content{std::istreambuf_iterator<char>{input},
                              std::istreambuf_iterator<char>{}};
    if (input.bad()) {
        std::println(stderr, "File read failed");
        return 1;
    }
    std::println("Bytes read: {}", content.size());
}
