#include <iostream>
#include <memory>
#include <string>

int main() {
    auto owner = std::make_shared<std::string>("sensor-hub");
    std::weak_ptr<std::string> observer{owner};
    if (const auto active = observer.lock()) {
        std::cout << "Active: " << *active << '\n';
    }
    owner.reset();
    std::cout << std::boolalpha;
    std::cout << "Expired: " << observer.expired() << '\n';
}
