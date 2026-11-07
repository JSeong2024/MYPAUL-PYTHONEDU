#include <concepts>
#include <print>

// 조직 내 여러 장치가 같은 value()/valid() 계약을 제공한다고 가정.
template <typename T>
concept NumericReading = requires(const T& item) {
    { item.value() } -> std::convertible_to<double>;
    { item.valid() } -> std::convertible_to<bool>;
};

struct Temperature {
    double celsius;
    bool ok;
    [[nodiscard]] double value() const noexcept { return celsius; }
    [[nodiscard]] bool valid() const noexcept { return ok; }
};
struct Pressure {
    float kpa;
    bool ok;
    [[nodiscard]] float value() const noexcept { return kpa; }
    [[nodiscard]] bool valid() const noexcept { return ok; }
};

template <NumericReading T>
[[nodiscard]] bool exceeds(const T& reading, double threshold) {
    return reading.valid() && static_cast<double>(reading.value()) > threshold;
}

int main() {
    std::println("Temperature alarm: {}", exceeds(Temperature{32.1, true}, 30.0));
    std::println("Pressure alarm: {}", exceeds(Pressure{118.0f, false}, 100.0));
}
