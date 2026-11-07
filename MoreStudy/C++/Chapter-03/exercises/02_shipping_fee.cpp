#include <charconv>
#include <iostream>
#include <print>
#include <string>
#include <system_error>

int main() {
    constexpr int unit_price_won{12'900};
    constexpr int free_shipping_won{50'000};
    constexpr int shipping_fee_won{3'000};

    std::cout << "Quantity (1-20): " << std::flush;
    std::string line;
    if (!std::getline(std::cin, line)) {
        std::cerr << "Error: missing input.\n";
        return 1;
    }

    int quantity{};
    const auto parsed = std::from_chars(
        line.data(), line.data() + line.size(), quantity);
    if (parsed.ec != std::errc{} ||
        parsed.ptr != line.data() + line.size() ||
        quantity < 1 || quantity > 20) {
        std::cerr << "Error: invalid quantity.\n";
        return 1;
    }

    // TODO: subtotal, shipping fee and final total.
    (void)unit_price_won;
    (void)free_shipping_won;
    (void)shipping_fee_won;
    std::println("TODO: calculate order total");
}
