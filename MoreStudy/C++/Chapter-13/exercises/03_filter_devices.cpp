#include <print>
#include <ranges>
#include <string>
#include <vector>

struct Device { std::string name; int priority; };

// TODO: std::ranges::sort 및 Projection으로 priority 내림차순 정렬
// TODO: std::views::filter와 std::ranges::to로 우선순위 3 이상만 추출
int main() {
    std::vector<Device> devices{{"camera", 3}, {"motor", 1}, {"lidar", 5}};
    // TODO
    std::println("Device count: {}", devices.size());
}
