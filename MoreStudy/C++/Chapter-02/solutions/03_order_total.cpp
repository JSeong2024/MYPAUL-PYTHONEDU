#include <charconv>
#include <cstdint>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    constexpr std::int64_t unit_price_won{12'900};
    std::cout << "Quantity (1-100): " << std::flush;

    std::string input;
    if (!std::getline(std::cin, input)) {
        std::cerr << "Error: unable to read input.\n";
        return 1;
    }

    std::int64_t quantity{};
    const char* const end = input.data() + input.size();
    const auto [next, error] =
        std::from_chars(input.data(), end, quantity);

    if (error != std::errc{} || next != end ||
        quantity < 1 || quantity > 100) {
        std::cerr << "Error: enter an integer from 1 to 100.\n";
        return 1;
    }

    const std::int64_t total_won{unit_price_won * quantity};
    std::println("Total: {} KRW", total_won);
}
