#include <print>
#include <string_view>

class Base {
public:
    Base() { std::println("During Base construction: {}", name()); }
    virtual ~Base() = default;
    [[nodiscard]] virtual std::string_view name() const noexcept {
        return "Base";
    }
};

class Derived final : public Base {
public:
    [[nodiscard]] std::string_view name() const noexcept override {
        return "Derived";
    }
};

int main() {
    const Derived derived;
    std::println("After construction: {}", derived.name());
}
