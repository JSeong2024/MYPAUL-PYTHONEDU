#include <iostream>
#include <string>

int main() {
    constexpr int capacity{100};
    const std::string device_name{"Counter-01"};
    auto recorded_count = 12;

    std::cout << "Device: " << device_name << '\n';
    std::cout << "Capacity: " << capacity << '\n';
    std::cout << "Recorded: " << recorded_count << '\n';

    recorded_count = 15;
    std::cout << "Updated: " << recorded_count << '\n';
}
