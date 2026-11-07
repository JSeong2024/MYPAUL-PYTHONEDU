#include <concepts>
#include <print>
#include <string>
#include <string_view>

// 장치 이름을 문자열 뷰로 읽을 수 있는지만 컴파일 시점에 검사
template <typename T>
concept NamedDevice = requires(const T& value) {
    { value.name() } -> std::convertible_to<std::string_view>;
};

struct Device {
    std::string label{"Motor-A"};
    [[nodiscard]] std::string_view name() const noexcept { return label; }
};

struct AnonymousDevice { int id{1}; };
static_assert(NamedDevice<Device>);
static_assert(!NamedDevice<AnonymousDevice>);

template <NamedDevice T>
void print_name(const T& value) {
    std::println("Device: {}", value.name());
}

int main() {
    print_name(Device{});
}
