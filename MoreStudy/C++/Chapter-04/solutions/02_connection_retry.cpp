#include <array>
#include <cstddef>
#include <cstddef>
#include <cstddef>
#include <print>

int main() {
    constexpr std::array responses{false, false, true, false, true};
    constexpr std::size_t max_attempts{4};
    bool connected{false};

    for (std::size_t attempt{0};
         attempt < max_attempts && attempt < responses.size(); ++attempt) {
        if (responses[attempt]) {
            std::println("Connected on attempt {}", attempt + 1);
            connected = true;
            break;
        }
    }

    if (!connected) {
        std::println("Connection failed");
        return 1;
    }
}
