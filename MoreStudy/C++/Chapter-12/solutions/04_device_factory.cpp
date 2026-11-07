#include <expected>
#include <memory>
#include <print>
#include <string>
#include <string_view>

struct Device {
    std::string name;
    int interval_ms{};
};

[[nodiscard]] std::expected<std::unique_ptr<Device>, std::string>
create_device(std::string_view name, int interval_ms) {
    if (name.empty()) return std::unexpected("empty device name");
    if (interval_ms < 1 || interval_ms > 1'000) {
        return std::unexpected("interval must be 1..1000 ms");
    }
    return std::make_unique<Device>(Device{std::string{name}, interval_ms});
}

int main() {
    auto ok = create_device("lidar", 50);
    if (ok) std::println("Device: {} ({} ms)", (*ok)->name, (*ok)->interval_ms);
    auto bad = create_device("", 0);
    if (!bad) std::println("Error: {}", bad.error());
}
