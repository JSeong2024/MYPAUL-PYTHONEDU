#include <iostream>
#include <span>
#include <stdexcept>
#include <utility>
#include <vector>

class ReadingStore {
public:
    explicit ReadingStore(std::vector<int> values) : values_(std::move(values)) {}
    void replace(std::span<const int> incoming) {
        std::vector<int> staged{incoming.begin(), incoming.end()};
        for (int value : staged) {
            if (value < 0 || value > 100) {
                throw std::invalid_argument("reading outside 0..100");
            }
        }
        values_.swap(staged); // 검증이 끝나면 한 번에 교체
    }
    [[nodiscard]] int first() const { return values_.at(0); }
private:
    std::vector<int> values_;
};

int main() {
    ReadingStore store{{10, 20}};
    const int incoming[]{30, 130};
    try {
        store.replace(incoming);
    } catch (const std::invalid_argument&) {
        std::cout << "Rejected\n";
    }
    std::cout << "First: " << store.first() << '\n';
}
