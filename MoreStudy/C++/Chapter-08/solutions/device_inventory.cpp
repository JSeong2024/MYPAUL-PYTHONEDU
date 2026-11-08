#include <cstddef>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

struct Device {
    std::string id;
    int power_w{};
    bool online{};
};

class DeviceInventory {
public:
    [[nodiscard]] bool add(std::string id, int power_w, bool online) {
        if (id.empty() || power_w < 0 || power_w > 2'000) {
            return false;
        }
        for (const Device& device : devices_) {
            if (device.id == id) {
                return false;
            }
        }
        devices_.push_back(Device{std::move(id), power_w, online});
        return true;
    }

    [[nodiscard]] std::size_t size() const noexcept { return devices_.size(); }

    [[nodiscard]] int online_count() const noexcept {
        int count{};
        for (const Device& device : devices_) {
            if (device.online) {
                ++count;
            }
        }
        return count;
    }

    [[nodiscard]] int total_power() const noexcept {
        int total{};
        for (const Device& device : devices_) {
            total += device.power_w;
        }
        return total;
    }

    [[nodiscard]] int active_power() const noexcept {
        int total{};
        for (const Device& device : devices_) {
            if (device.online) {
                total += device.power_w;
            }
        }
        return total;
    }

    [[nodiscard]] const Device* highest_power() const noexcept {
        if (devices_.empty()) {
            return nullptr;
        }
        const Device* highest{&devices_.front()};
        for (const Device& device : devices_) {
            if (device.power_w > highest->power_w) {
                highest = &device;
            }
        }
        return highest;
    }

private:
    std::vector<Device> devices_;
};

int main() {
    std::cout << "Devices (1-5): " << std::flush;
    int count{};
    if (!(std::cin >> count) || count < 1 || count > 5) {
        std::cerr << "Error: invalid device count.\n";
        return 1;
    }

    DeviceInventory inventory;
    for (int i{1}; i <= count; ++i) {
        std::cout << "Device " << i << " (ID power_W online_0_or_1): "
                  << std::flush;
        std::string id;
        int power{};
        int online{};
        if (!(std::cin >> id >> power >> online) ||
            (online != 0 && online != 1)) {
            std::cerr << "Error: invalid device input.\n";
            return 1;
        }
        if (!inventory.add(std::move(id), power, online == 1)) {
            std::cerr << "Error: invalid or duplicate device.\n";
            return 1;
        }
    }

    const Device* highest{inventory.highest_power()};
    std::cout << "\n--- Device Inventory ---\n";
    std::cout << "Registered: " << inventory.size() << '\n';
    std::cout << "Online: " << inventory.online_count() << '\n';
    std::cout << "Total power: " << inventory.total_power() << " W\n";
    std::cout << "Active power: " << inventory.active_power() << " W\n";
    if (highest != nullptr) {
        std::cout << "Highest power: " << highest->id << " ("
                  << highest->power_w << " W)\n";
    }
}
