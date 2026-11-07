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
    // TODO: 이름이 비어 있거나 주기가 1~1000 범위를 벗어나면 오류 반환
    // TODO: 유효한 요청이면 Device의 Exclusive Ownership 반환
    (void)name;
    (void)interval_ms;
    return std::unexpected("not implemented");
}

int main() {
    auto ok = create_device("lidar", 50);
    if (ok) std::println("Device: {}", (*ok)->name);
    auto bad = create_device("", 0);
    if (!bad) std::println("Error: {}", bad.error());
}
