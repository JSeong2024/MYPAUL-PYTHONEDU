#include <print>

struct CelsiusTag {};
struct KilopascalTag {};

// TODO: Tag와 T를 받는 Quantity 클래스를 정의.
// - explicit 생성자
// - value() const
// - 같은 Tag/T끼리만 가능한 operator+

template <typename Tag, typename T>
struct Quantity {
    T measurement;
    explicit Quantity(T value) : measurement(value) {}
    [[nodiscard]] T value() const { return measurement; }
    // TODO: operator+ 구현
};

int main() {
    Quantity<CelsiusTag, double> a{21.0};
    Quantity<CelsiusTag, double> b{1.5};
    // TODO: a + b를 사용하여 22.5 출력
    std::println("Temperature: {}", a.value() + b.value());
}
