#include <array>
#include <print>
#include <stdexcept>

int main() {
    const std::array<int, 3> voltages{12, 24, 48};
    const std::size_t requested_index{3};

    if (requested_index >= voltages.size()) {
        std::println("Index {} is out of range", requested_index);
    }

    try {
        std::println("Voltage: {}", voltages.at(requested_index));
    } catch (const std::out_of_range&) {
        std::println("Access rejected by at()");
    }
}
