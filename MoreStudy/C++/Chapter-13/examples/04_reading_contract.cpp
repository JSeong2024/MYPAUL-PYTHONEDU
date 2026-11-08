#include <concepts>
#include <iostream>

template <typename T>
concept ReadingLike = requires(const T& reading) {
    { reading.value() } -> std::convertible_to<double>;
    { reading.valid() } -> std::convertible_to<bool>;
};

struct Temperature {
    double degrees;
    bool okay;
    [[nodiscard]] double value() const { return degrees; }
    [[nodiscard]] bool valid() const { return okay; }
};

static_assert(ReadingLike<Temperature>);
static_assert(!ReadingLike<int>);

template <ReadingLike T>
[[nodiscard]] bool needs_attention(const T& item) {
    return item.valid() && item.value() >= 80.0;
}

int main() {
    std::cout << std::boolalpha << "Alert: "
              << needs_attention(Temperature{85.0, true}) << '\n';
}
