#include <array>
#include <print>
#include <span>
#include <vector>

[[nodiscard]] double average(std::span<const int> values) noexcept {
    if (values.empty()) {
        return 0.0; // 이 API에서는 빈 구간을 0으로 정의
    }

    double sum{0.0};
    for (const int value : values) {
        sum += value;
    }
    return sum / static_cast<double>(values.size());
}

int main() {
    const std::array fixed{10, 20, 30};
    const std::vector dynamic{40, 50, 60};
    std::println("Fixed: {:.1f}", average(fixed));
    std::println("Dynamic: {:.1f}", average(dynamic));
}
