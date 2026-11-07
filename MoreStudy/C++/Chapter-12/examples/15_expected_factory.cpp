#include <expected>
#include <memory>
#include <print>
#include <string>
#include <string_view>
#include <utility>

struct Device {
    std::string id;
    explicit Device(std::string value) : id(std::move(value)) {}
};

[[nodiscard]] std::expected<std::unique_ptr<Device>, std::string>
connect(std::string_view id) {
    if (id.empty()) return std::unexpected("empty id");
    return std::make_unique<Device>(std::string{id});
}

int main() {
    auto result = connect("camera-A");
    if (result) std::println("Connected: {}", (*result)->id);
    auto failed = connect("");
    if (!failed) std::println("Rejected: {}", failed.error());
}
