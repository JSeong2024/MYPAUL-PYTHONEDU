#include <span>
#include <stdexcept>
#include <utility>
#include <vector>
#ifndef CH12_LIBRARY_ONLY
#include <iostream>
#endif

class SensorStore {
public:
    explicit SensorStore(std::vector<int> values) : values_(std::move(values)) {}

    void replace(std::span<const int> incoming) {
        std::vector<int> staged{incoming.begin(), incoming.end()};
        if (staged.empty()) throw std::invalid_argument("empty batch");
        for (int value : staged) {
            if (value < 0 || value > 100) throw std::invalid_argument("reading outside 0..100");
        }
        values_.swap(staged);
    }
    [[nodiscard]] const std::vector<int>& values() const noexcept { return values_; }
private:
    std::vector<int> values_;
};

#ifndef CH12_LIBRARY_ONLY
int main() {
    SensorStore store{{10, 20}};
    const int invalid[]{30, 130};
    try { store.replace(invalid); }
    catch (const std::invalid_argument&) { std::cout << "Rejected\n"; }
    std::cout << "First: " << store.values().at(0) << '\n';
    const int valid[]{60, 80};
    store.replace(valid);
    std::cout << "Updated: " << store.values().at(0) << '\n';
}
#endif
