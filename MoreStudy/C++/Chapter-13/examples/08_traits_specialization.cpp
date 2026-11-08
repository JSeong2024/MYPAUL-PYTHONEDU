#include <iostream>
#include <string_view>
#include <type_traits>

template <typename T>
struct TypeLabel {
    static constexpr std::string_view name = "other";
};

template <>
struct TypeLabel<int> {
    static constexpr std::string_view name = "integer";
};

template <typename T>
constexpr bool arithmetic_value = std::is_arithmetic_v<T>;

int main() {
    std::cout << std::boolalpha;
    std::cout << "Arithmetic: " << arithmetic_value<double> << '\n';
    std::cout << "Label: " << TypeLabel<int>::name << '\n';
    std::cout << "Other: " << TypeLabel<std::string_view>::name << '\n';
}
