#include <algorithm>
#include <print>
#include <string_view>

void set_motor_speed(int& current_rpm, int requested_rpm) noexcept {
    current_rpm = std::clamp(requested_rpm, 0, 3'000);
}

void print_motor_status(std::string_view name, int rpm) {
    std::println("{}: {} RPM", name, rpm);
}

int main() {
    int current_rpm{1'200};
    set_motor_speed(current_rpm, 3'500);
    print_motor_status("Motor-A", current_rpm);
}
