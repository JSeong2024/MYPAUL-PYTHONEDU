#include <concepts>
#include <iostream>

template <std::integral... Ts>
[[nodiscard]] long long sum_all(Ts... values) {
    return (0LL + ... + static_cast<long long>(values));
}

int main() {
    std::cout << "Total: " << sum_all(4, 7, 9) << '\n';
    std::cout << "Empty: " << sum_all() << '\n';
}
