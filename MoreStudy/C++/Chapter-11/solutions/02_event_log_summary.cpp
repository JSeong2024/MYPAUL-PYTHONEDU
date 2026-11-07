#include <array>
#include <fstream>
#include <print>
#include <string>
#include <string_view>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    constexpr std::array<std::string_view, 3> levels{"INFO", "WARN", "ERROR"};
    std::array<std::size_t, 3> counts{};
    std::string line;
    std::size_t line_number{};
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') line.pop_back();
        const auto first = line.find('|');
        if (first == std::string::npos) return 1;
        const auto second = line.find('|', first + 1);
        if (second == std::string::npos || first == 0 ||
            second == first + 1 || second + 1 == line.size()) return 1;
        const std::string_view level{line.data(), first};
        bool matched = false;
        for (std::size_t i = 0; i < levels.size(); ++i) {
            if (level == levels[i]) {
                ++counts[i];
                matched = true;
                break;
            }
        }
        if (!matched) {
            std::println(stderr, "Invalid level at line {}", line_number);
            return 1;
        }
    }
    if (input.bad()) return 1;
    for (std::size_t i = 0; i < levels.size(); ++i) {
        std::println("{}: {}", levels[i], counts[i]);
    }
}
