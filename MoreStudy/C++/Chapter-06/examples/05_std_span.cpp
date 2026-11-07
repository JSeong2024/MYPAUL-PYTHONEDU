#include <array>
#include <print>
#include <span>
#include <vector>

[[nodiscard]] long long total_samples(std::span<const int> samples) {
    long long total{};
    for (const int value : samples) {
        total += value;
    }
    return total;
}

void apply_offset(std::span<int> samples, int offset) {
    for (int& value : samples) {
        value += offset;  // 예제에서는 결과가 int 범위를 벗어나지 않음.
    }
}

int main() {
    std::array<int, 3> fixed{10, 20, 30};
    std::vector<int> dynamic{5, 15};
    apply_offset(fixed, 2);

    std::println("Array total: {}", total_samples(fixed));
    std::println("Vector total: {}", total_samples(dynamic));
}
