#include <print>

struct Reading {
    double value;
    bool valid;
};

// TODO: 유효한 측정값이면서 threshold보다 엄격하게 큰 경우에만 true 반환.
[[nodiscard]] bool is_alert(const Reading& reading, double threshold) {
    (void)reading;
    (void)threshold;
    return false;
}

int main() {
    std::println("High: {}", is_alert({31.5, true}, 30.0));
    std::println("Invalid: {}", is_alert({40.0, false}, 30.0));
}
