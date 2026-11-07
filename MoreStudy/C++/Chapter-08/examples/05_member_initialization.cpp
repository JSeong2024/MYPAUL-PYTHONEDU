#include <print>
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
        std::println("{} on channel {}", name_, channel_);
    }

private:
    std::string name_;
    int channel_{};
};

int main() {
    const RetryOptions options{};
    const Device sensor{"LIDAR", 2};
    std::println("Retries: {}, delay: {} ms", options.attempts, options.delay_ms);
    sensor.print();
}
