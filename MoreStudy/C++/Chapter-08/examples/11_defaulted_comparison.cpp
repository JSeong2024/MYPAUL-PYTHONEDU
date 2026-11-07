#include <print>

struct DeviceKey {
    int rack{};
    int slot{};

    [[nodiscard]] bool operator==(const DeviceKey&) const = default;
};

int main() {
    const DeviceKey a{2, 7};
    const DeviceKey b{2, 7};
    const DeviceKey c{2, 8};
    std::println("a == b: {}", a == b);
    std::println("a == c: {}", a == c);
}
