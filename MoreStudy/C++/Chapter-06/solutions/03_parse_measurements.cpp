#include <algorithm>
#include <charconv>
#include <expected>
#include <iostream>
#include <print>
#include <string>
#include <string_view>
#include <vector>

[[nodiscard]] std::string_view trim_ascii(std::string_view text) {
    constexpr std::string_view spaces{" \t\r\n"};
    const auto first = text.find_first_not_of(spaces);
    if (first == std::string_view::npos) {
        return {};
    }
    const auto last = text.find_last_not_of(spaces);
    return text.substr(first, last - first + 1);
}

[[nodiscard]] std::expected<int, std::string_view> parse_value(std::string_view text) {
    text = trim_ascii(text);
    int value{};
    const auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (error != std::errc{} || end != text.data() + text.size()) {
        return std::unexpected("invalid number");
    }
    if (value < -100 || value > 100) {
        return std::unexpected("number out of range");
    }
    return value;
}

int main() {
    std::string line;
    if (!std::getline(std::cin, line) || line.size() > 1'000) {
        std::println(stderr, "Invalid input");
        return 1;
    }

    std::vector<int> values;
    std::string_view remaining{line};
    while (true) {
        const auto delimiter = remaining.find(',');
        const auto field = remaining.substr(0, delimiter);
        const auto parsed = parse_value(field);
        if (!parsed || values.size() >= 100) {
            std::println(stderr, "Invalid measurement list");
            return 1;
        }
        values.push_back(*parsed);
        if (delimiter == std::string_view::npos) {
            break;
        }
        remaining.remove_prefix(delimiter + 1);
    }

    long long sum{};
    for (int value : values) {
        sum += value;
    }
    std::println("Samples: {}", values.size());
    std::println("Average: {:.2f}", static_cast<double>(sum) / values.size());
    std::println("Peak: {}", *std::ranges::max_element(values));
}
