#include <cstdint>
#include <iostream>
#include <string>

int main() {
    const std::string name{"Sensor-A1"};
    const std::uint32_t id{1'024};
    const bool ready{true};

    std::cout << std::boolalpha;
    std::cout << "Device: " << name << '\n';
    std::cout << "ID: " << id << '\n';
    std::cout << "Ready: " << ready << '\n';
}
