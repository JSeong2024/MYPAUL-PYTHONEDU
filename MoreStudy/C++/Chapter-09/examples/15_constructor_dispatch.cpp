#include <iostream>

class Base {
public:
    Base() { std::cout << "Base constructor: " << label() << '\n'; }
    virtual ~Base() = default;
    [[nodiscard]] virtual const char* label() const noexcept { return "base"; }
};
class Derived final : public Base {
public:
    Derived() { std::cout << "Derived constructor: " << label() << '\n'; }
    [[nodiscard]] const char* label() const noexcept override { return "derived"; }
};
int main() {
    const Derived item;
    std::cout << "After construction: " << item.label() << '\n';
}
