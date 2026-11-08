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
        // TODO: 빈 ID, 범위 밖의 전력, 중복 ID를 거절하세요.
        // TODO: 유효한 장치는 devices_에 추가하세요.
        (void)id;
        (void)power_w;
        (void)online;
        return false;
    }

    [[nodiscard]] std::size_t size() const noexcept { return devices_.size(); }

    [[nodiscard]] int online_count() const noexcept {
        // TODO: 온라인 장치의 개수를 구하세요.
        return 0;
    }

    [[nodiscard]] int total_power() const noexcept {
        // TODO: 등록된 모든 장치의 소비 전력을 합산하세요.
        return 0;
    }

    [[nodiscard]] int active_power() const noexcept {
        // TODO: 온라인 장치의 소비 전력만 합산하세요.
        return 0;
    }

    [[nodiscard]] const Device* highest_power() const noexcept {
        // TODO: 소비 전력이 가장 큰 장치의 주소를 반환하세요.
        // 빈 목록은 nullptr를 반환하고, 동점이면 먼저 등록한 장치를 선택하세요.
        return nullptr;
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
