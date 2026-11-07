#include <expected>
#include <fstream>
#include <iterator>
#include <print>
#include <string>

[[nodiscard]] std::expected<std::string, std::string>
load_text(const std::string& path) {
    std::ifstream input{path};
    if (!input) return std::unexpected("Cannot open input file");
    std::string contents{std::istreambuf_iterator<char>{input},
                         std::istreambuf_iterator<char>{}};
    if (input.bad()) return std::unexpected("Read failed");
    return contents;
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    const auto text = load_text(argv[1]);
    if (!text) {
        std::println(stderr, "{}", text.error());
        return 1;
    }
    std::println("Loaded {} bytes", text->size());
}
