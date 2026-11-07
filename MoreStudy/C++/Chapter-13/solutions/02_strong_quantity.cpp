#include <print>

struct CelsiusTag {};
struct KilopascalTag {};

template <typename Tag, typename T>
class Quantity {
public:
    explicit constexpr Quantity(T value) : value_(value) {}
    [[nodiscard]] constexpr T value() const { return value_; }
    [[nodiscard]] constexpr Quantity operator+(Quantity other) const {
        return Quantity{value_ + other.value_};
    }
private:
    T value_;
};

int main() {
    const Quantity<CelsiusTag, double> a{21.0};
    const Quantity<CelsiusTag, double> b{1.5};
    const Quantity<KilopascalTag, double> pressure{101.3};
    std::println("Temperature: {}", (a + b).value());
    std::println("Pressure: {}", pressure.value());
    // a + pressure; // 타입이 달라 컴파일 실패
}
