#include <concepts>
#include <print>
#include <string>
#include <string_view>

// name()의 반환값이 string_view로 바뀔 수 있는 장치만 허용.
template <typename T>
concept NamedDevice = requires(const T& device) {
    { device.name() } -> std::convertible_to<std::string_view>;
};

struct Motor {
    std::string label{"motor-A"};
    [[nodiscard]] std::string_view name() const noexcept { return label; }
};
struct AnonymousDevice { int id{1}; };

static_assert(NamedDevice<Motor>);
static_assert(!NamedDevice<AnonymousDevice>);

template <NamedDevice T>
void print_device(const T& device) {
    std::println("Device: {}", device.name());
}

int main() {
    print_device(Motor{});
    // print_device(AnonymousDevice{}); // 제약 조건 불충족
}
