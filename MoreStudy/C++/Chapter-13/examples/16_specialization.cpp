#include <print>
#include <string_view>

template <typename T>
struct UnitLabel { static constexpr std::string_view value = "units"; };

template <>
struct UnitLabel<double> { static constexpr std::string_view value = "C"; };

template <typename T>
void show_measurement(const T& value) {
    std::println("{} {}", value, UnitLabel<T>::value);
}

int main() {
    show_measurement(5);
    show_measurement(22.5);
}
