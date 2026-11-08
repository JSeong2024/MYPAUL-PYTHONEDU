#include <iostream>
#include <optional>
#include <string>

std::optional<int> parse_time(const std::string& value) {
    if (value.size() != 5 || value[2] != ':') return std::nullopt;
    for (int i : {0, 1, 3, 4}) {
        if (value[i] < '0' || value[i] > '9') return std::nullopt;
    }
    const int hour = (value[0] - '0') * 10 + (value[1] - '0');
    const int minute = (value[3] - '0') * 10 + (value[4] - '0');
    if (hour > 23 || minute > 59) return std::nullopt;
    return hour * 60 + minute;
}

int main() {
    std::string entry, exit;
    if (!(std::cin >> entry >> exit)) {
        std::cout << "INVALID\n";
        return 0;
    }
    const auto start = parse_time(entry);
    const auto end = parse_time(exit);
    if (!start || !end || *end <= *start) {
        std::cout << "INVALID\n";
        return 0;
    }
    const int elapsed = *end - *start;
    const int extra_blocks = elapsed > 30 ? (elapsed - 30 + 9) / 10 : 0;
    std::cout << 1000 + extra_blocks * 500 << '\n';
}
