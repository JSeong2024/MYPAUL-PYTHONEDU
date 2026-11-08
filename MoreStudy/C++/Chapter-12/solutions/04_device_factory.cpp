#include <optional>
#include <string>
#include <utility>
#ifndef CH12_LIBRARY_ONLY
#include <iostream>
#endif

struct Device {
    std::string name;
    int limit{};
};

[[nodiscard]] std::optional<Device> make_device(std::string name, int limit) {
    if (name.empty() || name.size() > 16 || limit < 0 || limit > 100) {
        return std::nullopt;
    }
    for (unsigned char ch : name) {
        const bool allowed = (ch >= 'a' && ch <= 'z') ||
                             (ch >= 'A' && ch <= 'Z') ||
                             (ch >= '0' && ch <= '9') || ch == '-';
        if (!allowed) return std::nullopt;
    }
    return Device{std::move(name), limit};
}

#ifndef CH12_LIBRARY_ONLY
int main() {
    auto device = make_device("sensor-A", 80);
    if (device) std::cout << "Created: " << device->name << " / " << device->limit << '\n';
    if (!make_device("", 20)) std::cout << "Rejected empty name\n";
}
#endif
