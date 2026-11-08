#include <iostream>
#include <memory>
#include <string>
#include <utility>

template <typename T, typename... Args>
[[nodiscard]] std::unique_ptr<T> create(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

struct Device {
    explicit Device(std::string value) : name(std::move(value)) {}
    std::string name;
};

int main() {
    std::string name{"Pump-A"};
    auto first = create<Device>(name);         // lvalue: 복사 가능
    auto second = create<Device>(std::string{"Pump-B"}); // rvalue: 이동 가능
    std::cout << first->name << ", " << second->name << '\n';
}
