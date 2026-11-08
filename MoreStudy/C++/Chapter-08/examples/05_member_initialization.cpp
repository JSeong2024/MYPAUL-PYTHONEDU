#include <iostream>
#include <string>
#include <utility>

struct RetryOptions {
    int attempts{3};
    int delay_ms{250};
};

class Device {
public:
    Device(std::string name, int channel)
        : name_{std::move(name)}, channel_{channel} {}

    void print() const {
        std::cout << name_ << " on channel " << channel_ << '\n';
    }

private:
    std::string name_;
    int channel_{};
};

int main() {
    const RetryOptions options{};
    const Device sensor{"LIDAR", 2};
    std::cout << "Retries: " << options.attempts
              << ", delay: " << options.delay_ms << " ms\n";
    sensor.print();
}
