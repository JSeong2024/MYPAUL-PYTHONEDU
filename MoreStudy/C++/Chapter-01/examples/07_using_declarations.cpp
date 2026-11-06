#include <cstdint>
#include <print>
#include <string>

int main() {
    using std::println;             // 필요한 이름만 가져옴
    using std::string;
    using OrderId = std::uint64_t;  // 자료형 별칭

    const OrderId order_id{1001};
    const string customer{"Kim Min Su"};

    println("Order #{}: {}", order_id, customer);
    return 0;
}
