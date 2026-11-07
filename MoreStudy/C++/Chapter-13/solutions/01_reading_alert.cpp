#include <print>

struct Reading {
    double value;
    bool valid;
};

[[nodiscard]] bool is_alert(const Reading& reading, double threshold) {
    return reading.valid && reading.value > threshold;
}

int main() {
    std::println("High: {}", is_alert({31.5, true}, 30.0));
    std::println("Invalid: {}", is_alert({40.0, false}, 30.0));
}
