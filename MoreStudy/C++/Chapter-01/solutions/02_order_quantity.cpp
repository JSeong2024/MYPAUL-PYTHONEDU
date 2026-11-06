#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    std::string input;
    if (!std::getline(std::cin, input)) {
        std::cerr << "Error: unable to read input.\n";
        return 1;
    }

    int quantity{};
    const char* const end = input.data() + input.size();
    const auto [next, error] = std::from_chars(input.data(), end, quantity);

    if (error != std::errc{} || next != end ||
        quantity < 1 || quantity > 1000) {
        std::cerr << "Error: enter an integer from 1 to 1000.\n";
        return 1;
    }

    std::println("Order quantity: {}", quantity);
    return 0;
}
