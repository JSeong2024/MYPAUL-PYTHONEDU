#include <algorithm>
#include <print>
#include <string_view>
#include <vector>

struct Sensor {
    std::string_view id;
    int temperature;
};

int main() {
    const std::vector<Sensor> sensors{{"T-01", 31}, {"T-02", 72}, {"T-03", 42}};
    const auto hot = std::ranges::find_if(sensors, [](const Sensor& sensor) {
        return sensor.temperature >= 70;
    });
    if (hot != sensors.end()) {
        std::println("First alert: {}", hot->id);
    }
    const bool all_normal = std::ranges::all_of(sensors, [](const Sensor& sensor) {
        return sensor.temperature < 70;
    });
    std::println("All normal: {}", all_normal);
}
