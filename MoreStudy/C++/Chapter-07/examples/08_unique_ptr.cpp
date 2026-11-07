#include <memory>
#include <print>
#include <string>
#include <utility>

void consume_config(std::unique_ptr<std::string> config) {
    if (config) {
        std::println("Loaded config: {}", *config);
    }
}

int main() {
    auto config = std::make_unique<std::string>("motor.max_rpm=3000");
    consume_config(std::move(config));
    std::println("Ownership transferred: {}", config == nullptr);
}
