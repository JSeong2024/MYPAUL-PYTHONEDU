#include <algorithm>
#include <print>
#include <span>
#include <stdexcept>
#include <vector>

class SensorStore {
public:
    explicit SensorStore(std::vector<int> readings)
        : readings_(std::move(readings)) {}
    void replace(std::span<const int> incoming) {
        // TODO 1: incoming을 별도 임시 Container에 복사
        // TODO 2: 0~100 범위 이외의 값은 std::invalid_argument 예외 발생
        // TODO 3: 검증 성공 후 원본 데이터와 안전하게 교체
        (void)incoming;
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
}
