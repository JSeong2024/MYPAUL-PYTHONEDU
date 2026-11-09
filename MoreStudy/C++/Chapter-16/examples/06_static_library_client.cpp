#include <iostream>
#include <string>
[[nodiscard]] std::string format_device(const std::string& id, int count) {
    return id + ": " + std::to_string(count);
}
int main() {
    std::cout << format_device("sensor-A", 3) << '\n';
}
