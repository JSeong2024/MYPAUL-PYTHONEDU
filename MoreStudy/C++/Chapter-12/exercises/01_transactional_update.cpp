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
        // TODO 1: incoming을 새 std::vector에 복사합니다.
        // TODO 2: 비어 있거나 0~100 범위를 벗어난 값이 있으면 예외를 던집니다.
        // TODO 3: 모든 검증이 끝난 뒤 values_와 교체합니다.
        (void)incoming;
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
