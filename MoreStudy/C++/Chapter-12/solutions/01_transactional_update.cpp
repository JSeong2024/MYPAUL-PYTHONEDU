#include <algorithm>
#include <print>
#include <span>
#include <stdexcept>
#include <utility>
#include <vector>

class SensorStore {
public:
    explicit SensorStore(std::vector<int> readings)
        : readings_(std::move(readings)) {}
    void replace(std::span<const int> incoming) {
        std::vector<int> staged{incoming.begin(), incoming.end()};
        if (std::ranges::any_of(staged, [](int value) {
                return value < 0 || value > 100;
            })) {
            throw std::invalid_argument("out of range");
        }
        readings_.swap(staged);
    }
    [[nodiscard]] int first() const { return readings_.at(0); }
private:
    std::vector<int> readings_;
};

int main() {
    SensorStore store{{10, 20}};
    const int invalid[]{30, 130};
    try { store.replace(invalid); }
    catch (const std::invalid_argument&) { std::println("Rejected"); }
    std::println("First: {}", store.first());
    const int valid[]{60, 80};
    store.replace(valid);
    std::println("Updated: {}", store.first());
}
