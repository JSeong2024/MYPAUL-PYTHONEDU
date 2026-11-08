#include <iostream>
#include <optional>
#include <string>
#include <string_view>

struct Device {
    std::string id;
};

[[nodiscard]] std::optional<Device> create_device(std::string_view id) {
    if (id.empty()) return std::nullopt;
    return Device{std::string{id}};
}

int main() {
    auto device = create_device("sensor-A");
    if (device) std::cout << "Created: " << device->id << '\n';
    if (!create_device("")) std::cout << "Rejected empty id\n";
}
