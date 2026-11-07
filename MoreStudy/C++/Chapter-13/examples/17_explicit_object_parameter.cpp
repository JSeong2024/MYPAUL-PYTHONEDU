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
    counter.get() = 9;  // lvalue 객체는 수정 가능한 참조로 반환
    const Counter fixed{4};
    std::println("Mutable: {}, const: {}", counter.get(), fixed.get());
}
