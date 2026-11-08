#include <charconv>
#include <iostream>
#include <string>
#include <string_view>
#include <system_error>
#include <vector>

[[nodiscard]] bool parse_number(std::string_view field, int& result) {
    const auto start = field.find_first_not_of(' ');
    if (start == std::string_view::npos) return false;
    const auto end = field.find_last_not_of(' ');
    field = field.substr(start, end - start + 1);
    const char* first = field.data();
    const char* last = first + field.size();
    const auto [next, error] = std::from_chars(first, last, result);
    return error == std::errc{} && next == last && result >= -100 && result <= 100;
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line)) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    std::vector<int> numbers;
    const std::string_view text{line};
    std::size_t start{};
    while (true) {
        const auto comma = text.find(',', start);
        const auto count = comma == std::string_view::npos ? text.size() - start : comma - start;
        int value{};
        if (numbers.size() == 10 || !parse_number(text.substr(start, count), value)) {
            std::cerr << "Error: invalid input.\n";
            return 1;
        }
        numbers.push_back(value);
        if (comma == std::string_view::npos) break;
        start = comma + 1;
    }
    int total{};
    for (const int value : numbers) total += value;
    std::cout << "Count: " << numbers.size() << '\n';
    std::cout << "Sum: " << total << '\n';
}
