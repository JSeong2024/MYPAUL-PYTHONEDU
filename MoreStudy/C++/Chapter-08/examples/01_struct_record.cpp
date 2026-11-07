#include <print>
#include <string>

struct SensorReading {
    std::string device_id;
    double temperature_c{};
    bool online{};
};

int main() {
    const SensorReading reading{"TEMP-A", 23.5, true};
    std::println("{}: {:.1f} C (online: {})",
                 reading.device_id, reading.temperature_c, reading.online);
}
