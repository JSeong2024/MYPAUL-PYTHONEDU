#include <memory>
#include <print>
#include <string>

int main() {
    auto owner = std::make_shared<std::string>("sensor-hub");
    std::weak_ptr<std::string> observer = owner;

    if (const auto locked = observer.lock()) {
        std::println("Active: {}", *locked);
    }

    owner.reset();
    std::println("Expired: {}", observer.expired());
}
