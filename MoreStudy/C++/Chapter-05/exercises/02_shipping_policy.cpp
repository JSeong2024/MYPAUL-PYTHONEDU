#include <iostream>
#include <optional>
#include <print>

[[nodiscard]] std::optional<int>
shipping_fee(int order_won, bool remote_area) noexcept {
    // TODO: 음수 주문 금액은 std::nullopt 반환
    // TODO: 50,000원 이상은 기본 배송비(3,000원) 면제
    // TODO: 도서·산간 추가 배송비(2,000원)는 별도 적용
    (void)order_won;
    (void)remote_area;
    return std::nullopt;
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
