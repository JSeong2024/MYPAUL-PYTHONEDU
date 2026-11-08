#include <iostream>
#include <optional>

// TODO: 음수 금액 또는 0/1이 아닌 지역 구분값은 std::nullopt를 반환합니다.
// 일반 배송비 3000원, 50000원 이상 무료 배송, 도서·산간은 2000원 추가.
std::optional<int> shipping_fee(int subtotal, int remote) {
    // TODO
    (void)subtotal;
    (void)remote;
    return std::nullopt;
}

int main() {
    int subtotal{};
    int remote{};
    if (!(std::cin >> subtotal >> remote)) {
        std::cerr << "Error: invalid order.\n";
        return 1;
    }
    const auto fee{shipping_fee(subtotal, remote)};
    if (!fee.has_value()) {
        std::cerr << "Error: invalid order.\n";
        return 1;
    }
    std::cout << "Shipping: " << *fee << " won\n";
}
