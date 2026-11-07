#include <print>
#include <utility>

struct Counter {
    int value{};

    template <typename Self>
    [[nodiscard]] decltype(auto) get(this Self&& self) noexcept {
        return (std::forward<Self>(self).value);
    }
};

int main() {
    Counter counter{7};
    counter.get() = 9;
    const Counter immutable{4};
    std::println("Mutable: {}, const: {}", counter.get(), immutable.get());
}
