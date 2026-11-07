#include <algorithm>
#include <print>
#include <string>
#include <vector>

struct Device {
    std::string id;
    int priority;
};

int main() {
    std::vector<Device> devices{{"motor", 2}, {"camera", 3}, {"radar", 1}, {"lidar", 4}};
    // TODO 1: std::ranges::sort + Projection으로 우선순위 내림차순 정렬.
    // TODO 2: std::views::filter로 우선순위 3 이상만 선택.
    // TODO 3: 독립적인 vector<Device> 생성 (ranges::to 또는 ranges::copy).
    const std::vector<Device> selected{}; // TODO: 교체
    std::println("Selected: {}", selected.size());
}
