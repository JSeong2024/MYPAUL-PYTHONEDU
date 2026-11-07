#include <concepts>
#include <print>

// 센서값이 같은 숫자여도 단위가 다르면 서로 다른 타입으로 구분.
struct CelsiusTag {};
struct KilopascalTag {};

template <typename Tag, std::floating_point T>
class Quantity {
public:
    explicit constexpr Quantity(T value) noexcept : value_(value) {}
    [[nodiscard]] constexpr T value() const noexcept { return value_; }
    [[nodiscard]] constexpr Quantity operator+(Quantity other) const noexcept {
        return Quantity{value_ + other.value_};
    }
private:
    T value_;
};

int main() {
    const Quantity<CelsiusTag, double> room{20.0};
    const Quantity<CelsiusTag, double> offset{1.5};
    const Quantity<KilopascalTag, double> pressure{101.3};
    std::println("Temperature: {} C", (room + offset).value());
    std::println("Pressure: {} kPa", pressure.value());
    // room + pressure; // 단위가 다른 타입은 더할 수 없음
}
