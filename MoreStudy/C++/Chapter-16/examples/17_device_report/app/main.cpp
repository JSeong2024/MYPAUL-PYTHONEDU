#include "device/report.hpp"
#include <array>
#include <iostream>
int main() {
    const std::array records{device::Record{"A", 35}, device::Record{"B", 92}, device::Record{"C", 58}};
    const device::Summary result = device::summarize(records, 80);
    std::cout << "Records: " << result.count << ", Alerts: " << result.alerts
              << ", Total: " << result.total << '\n';
}
