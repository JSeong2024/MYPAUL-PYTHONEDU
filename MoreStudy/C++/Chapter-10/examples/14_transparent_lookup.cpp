#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <string_view>

int main() {
    const std::map<std::string, int, std::less<>> inventory{{"camera", 2}, {"lidar", 4}};
    const std::string_view key{"lidar"};
    const auto found = inventory.find(key);  // string 임시 객체 없이 조회
    if (found != inventory.end()) {
        std::cout << found->first << ": " << found->second << '\n';
    }
    std::cout << std::boolalpha << "Has imu: " << inventory.contains("imu") << '\n';
}
