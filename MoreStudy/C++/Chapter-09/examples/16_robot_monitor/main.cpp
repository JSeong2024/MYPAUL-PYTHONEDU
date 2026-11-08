#include "monitor.hpp"
#include <iostream>
#include <memory>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    using monitor::Sensor;
    std::vector<std::unique_ptr<Sensor>> sensors;
    sensors.push_back(std::make_unique<monitor::TemperatureSensor>(75));
    sensors.push_back(std::make_unique<monitor::DistanceSensor>(22));
    sensors.push_back(std::make_unique<monitor::TemperatureSensor>(85));
    const monitor::Report report = monitor::evaluate(sensors);
    if (argc > 1 && std::string{argv[1]} == "--self-test") {
        return (report.total == 3 && report.alerts == 2) ? 0 : 1;
    }
    std::cout << "--- Robot Sensor Monitor ---\n";
    for (const auto& sensor : sensors) {
        std::cout << sensor->kind() << ' ' << sensor->reading() << ": "
                  << (sensor->alert() ? "ALERT" : "CLEAR") << '\n';
    }
    std::cout << "Total: " << report.total << '\n';
    std::cout << "Alerts: " << report.alerts << '\n';
}
