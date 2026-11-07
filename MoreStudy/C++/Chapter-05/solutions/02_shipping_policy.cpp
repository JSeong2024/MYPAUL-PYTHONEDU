#include <iostream>
#include <optional>
#include <print>

[[nodiscard]] std::optional<int>
shipping_fee(int order_won, bool remote_area) noexcept {
    if (order_won < 0) {
        return std::nullopt;
    }

    const int base_fee = order_won >= 50'000 ? 0 : 3'000;
    const int extra_fee = remote_area ? 2'000 : 0;
    return base_fee + extra_fee;
}

int main() {
    int order_won{};
    int remote_area_flag{};
    std::cout << "Order (won) and remote area (0/1): " << std::flush;
    if (!(std::cin >> order_won >> remote_area_flag) ||
        (remote_area_flag != 0 && remote_area_flag != 1)) {
        std::println("Invalid input");
        return 1;
    }

    const auto fee = shipping_fee(order_won, remote_area_flag == 1);
    if (!fee) {
        std::println("Invalid order amount");
        return 1;
    }
    std::println("Shipping: {} won", *fee);
}
