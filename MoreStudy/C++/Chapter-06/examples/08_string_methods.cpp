#include <iostream>
#include <string>

int main() {
    std::string device{"SENSOR-ROOM-07"};
    std::cout << std::boolalpha;
    std::cout << "Prefix: " << device.starts_with("SENSOR-") << '\n';
    std::cout << "Suffix: " << device.ends_with("-07") << '\n';
    std::cout << "Contains ROOM: " << (device.find("ROOM") != std::string::npos) << '\n';
    const auto first_dash = device.find('-');
    std::cout << "Category: " << device.substr(0, first_dash) << '\n';
    device += "-A";
    std::cout << "Updated: " << device << '\n';
}
