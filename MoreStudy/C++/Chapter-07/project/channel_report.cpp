#include <array>
#include <iomanip>
#include <iostream>
#include <span>

[[nodiscard]] int* select_channel(std::span<int> readings, int channel) noexcept {
    // TODO: return nullptr for channel 0 or invalid; otherwise the element address.
    (void)readings;
    (void)channel;
    return nullptr;
}

[[nodiscard]] bool apply_adjustment(int& reading, int delta) noexcept {
    // TODO: keep reading unchanged when adjusted value would be outside 0..100.
    (void)reading;
    (void)delta;
    return false;
}

[[nodiscard]] double average_reading(std::span<const int> readings) noexcept {
    // TODO: calculate the mean with a read-only span.
    (void)readings;
    return 0.0;
}

int main() {
    std::array<int, 3> readings{};
    std::cout << "Readings (3 values, 0-100): " << std::flush;
    if (!(std::cin >> readings[0] >> readings[1] >> readings[2])) {
        std::cerr << "Error: invalid input.\n";
        return 1;
    }
    for (const int value : readings) {
        if (value < 0 || value > 100) {
            std::cerr << "Error: reading out of range.\n";
            return 1;
        }
    }
    int channel{};
    std::cout << "Channel (0-3): " << std::flush;
    if (!(std::cin >> channel) || channel < 0 || channel > 3) {
        std::cerr << "Error: invalid channel.\n";
        return 1;
    }
    int delta{};
    std::cout << "Adjustment (-20 to 20): " << std::flush;
    if (!(std::cin >> delta) || delta < -20 || delta > 20) {
        std::cerr << "Error: invalid adjustment.\n";
        return 1;
    }

    int* selected{select_channel(readings, channel)};
    int before{};
    if (selected != nullptr) {
        before = *selected;
        if (!apply_adjustment(*selected, delta)) {
            std::cerr << "Error: adjusted reading out of range.\n";
            return 1;
        }
    }

    std::cout << "\n--- Channel Report ---\n";
    if (selected == nullptr) {
        std::cout << "Selected: NONE\n";
    } else {
        std::cout << "Selected: " << channel << '\n';
        std::cout << "Before: " << before << '\n';
        std::cout << "After: " << *selected << '\n';
    }
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Average: " << average_reading(readings) << '\n';
    if (selected == nullptr) {
        std::cout << "Status: NO CHANNEL\n";
    } else {
        std::cout << "Status: " << (*selected >= 80 ? "ALERT" : "NORMAL") << '\n';
    }
}
