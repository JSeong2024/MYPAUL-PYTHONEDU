#include <iostream>
#include <string>

struct SensorReading {
    std::string device_id;
    double temperature_c{};
    bool online{};
};

int main() {
    const SensorReading reading{"TEMP-A", 23.5, true};
    std::cout << std::boolalpha;
    std::cout << reading.device_id << ": " << reading.temperature_c
              << " C (online: " << reading.online << ")\n";
}
