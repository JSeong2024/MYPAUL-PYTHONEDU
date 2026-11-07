#include <algorithm>
#include <print>
#include <span>
#include <stdexcept>
#include <vector>
#include <utility>

class Readings {
public:
    explicit Readings(std::vector<int> values) : values_(std::move(values)) {}
    void replace(std::span<const int> values) {
        std::vector<int> staged{values.begin(), values.end()};
        if (std::ranges::any_of(staged, [](int x) { return x < 0; })) {
            throw std::invalid_argument("negative reading");
        }
        values_.swap(staged); // 검증이 끝난 뒤 한번에 교체
    }
    [[nodiscard]] int first() const { return values_.at(0); }
private:
    std::vector<int> values_;
};

int main() {
    Readings batch{{10, 20}};
    try {
        const int invalid[] = {3, -4};
        batch.replace(invalid);
    } catch (const std::invalid_argument&) {
        std::println("Rejected");
    }
    std::println("First unchanged: {}", batch.first());
}
