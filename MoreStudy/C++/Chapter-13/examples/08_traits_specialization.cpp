#include <concepts>
#include <print>
#include <string_view>
#include <type_traits>

struct TemperatureTag {};
struct PressureTag {};

// 도메인의 '단위 종류'를 타입으로 구분하고 문자열 정책을 제공.
template <typename Tag>
struct UnitLabel;

template <>
struct UnitLabel<TemperatureTag> {
    static constexpr std::string_view text = "C";
};
template <>
struct UnitLabel<PressureTag> {
    static constexpr std::string_view text = "kPa";
};

template <typename Tag, std::floating_point T>
void show_reading(T value) {
    static_assert(std::is_floating_point_v<T>);
    std::println("{} {}", value, UnitLabel<Tag>::text);
}

int main() {
    show_reading<TemperatureTag>(23.5);
    show_reading<PressureTag>(101.3);
}
