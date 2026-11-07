#include <print>
#include <string>
#include <string_view>
#include <vector>

// 문제: 장치가 존재하면 해당 문자열을 가리키는 포인터, 없으면 nullptr.
// 호출자는 벡터의 요소가 무효화되는 변경을 수행하기 전에 포인터 사용을 끝냄.
[[nodiscard]] const std::string* find_device(
    const std::vector<std::string>& devices, std::string_view target) {
    // TODO: 선형 검색 후 주소 반환
    (void)devices;
    (void)target;
    return nullptr;
}

int main() {
    const std::vector<std::string> devices{"camera", "lidar", "imu"};
    if (const auto* found = find_device(devices, "imu")) {
        std::println("Found: {}", *found);
    }
    std::println("Missing: {}", find_device(devices, "gps") == nullptr);
}
