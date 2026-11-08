#include <iostream>

struct DistanceTag {};
struct TimeTag {};

template <typename Tag>
class Quantity {
public:
    explicit Quantity(int value) : value_(value) {}
    [[nodiscard]] int value() const noexcept { return value_; }
    [[nodiscard]] Quantity operator+(const Quantity& other) const {
        return Quantity{value_ + other.value_};
    }
private:
    int value_{};
};
#ifndef CH13_LIBRARY_ONLY
int main() {
    const Quantity<DistanceTag> first{10};
    const Quantity<DistanceTag> second{15};
    std::cout << (first + second).value() << '\n';
}
#endif
