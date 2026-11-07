#include <print>
#include <string>
#include <type_traits>
#include <utility>

template <typename T>
struct Reading {
    T value;
};

template <typename T>
Reading(T) -> Reading<T>;  // 사용자 정의 Deduction Guide

int main() {
    std::pair item{std::string{"Motor-A"}, 125}; // CTAD
    Reading temperature{23.5};                  // CTAD
    static_assert(std::is_same_v<decltype(temperature.value), double>);
    std::println("{}: {} RPM", item.first, item.second);
    std::println("Temperature: {}", temperature.value);
}
