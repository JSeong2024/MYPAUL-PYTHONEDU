#include <charconv>
#include <cstdint>
#include <fstream>
#include <print>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;
    std::ifstream input{argv[1]};
    if (!input) return 1;
    std::string line;
    std::size_t count{};
    std::int64_t sum{};
    int minimum{}, maximum{};
    while (std::getline(input, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        int value{};
        const auto [end, error] = std::from_chars(line.data(), line.data() + line.size(), value);
        if (line.empty() || error != std::errc{} || end != line.data() + line.size() ||
            value < -1'000 || value > 1'000) {
            std::println(stderr, "Invalid value at line {}", count + 1);
            return 1;
        }
        if (count == 0) minimum = maximum = value;
        if (value < minimum) minimum = value;
        if (value > maximum) maximum = value;
        sum += value;
        ++count;
    }
    if (input.bad() || count == 0) return 1;
    std::println("Count: {}", count);
    std::println("Min: {}", minimum);
    std::println("Max: {}", maximum);
    std::println("Average: {:.2f}", static_cast<double>(sum) / count);
}
