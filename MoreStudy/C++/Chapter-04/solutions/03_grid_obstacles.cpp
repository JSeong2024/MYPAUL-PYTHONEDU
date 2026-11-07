#include <array>
#include <print>

int main() {
    constexpr std::array grid{
        std::array{0, 1, 0, 0},
        std::array{1, 0, 0, 1},
        std::array{0, 0, 1, 0}
    };
    int obstacles{};

    for (const auto& row : grid) {
        for (const int cell : row) {
            if (cell == 1) {
                ++obstacles;
            }
        }
    }

    std::println("Obstacles: {}", obstacles);
}
