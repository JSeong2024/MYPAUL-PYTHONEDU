#include <array>
#include <cstddef>
#include <print>

int main() {
    constexpr std::array responses{false, false, true, true};
    std::size_t attempt{};

    while (attempt < responses.size() && !responses[attempt]) {
        ++attempt;
    }

    if (attempt < responses.size()) {
        std::println("Connected on attempt {}", attempt + 1);
    } else {
        std::println("Connection failed");
        return 1;
    }
}
