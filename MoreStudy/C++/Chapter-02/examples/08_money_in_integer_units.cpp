#include <cstdint>
#include <limits>
#include <print>

int main() {
    constexpr std::int64_t unit_price_won{12'900};
    const std::int64_t quantity{3};

    if (quantity < 0 ||
        quantity > std::numeric_limits<std::int64_t>::max() / unit_price_won) {
        std::println("Error: invalid quantity.");
        return 1;
    }

    const std::int64_t total_won{unit_price_won * quantity};
    std::println("Total: {} KRW", total_won);
}
