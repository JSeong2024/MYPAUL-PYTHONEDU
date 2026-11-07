#include <memory>
#include <print>
#include <string>
#include <utility>

struct Device {
    explicit Device(std::string name) : name(std::move(name)) {}
    std::string name;
};

template <typename T, typename... Args>
[[nodiscard]] std::unique_ptr<T> create_owned(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

int main() {
    std::string name{"camera-A"};
    const auto device = create_owned<Device>(name);
    std::println("Created: {}", device->name);
}
