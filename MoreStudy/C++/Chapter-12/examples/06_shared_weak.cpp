#include <iostream>
#include <memory>

int main() {
    auto owner = std::make_shared<int>(42);
    std::weak_ptr<int> observer = owner;
    {
        auto second = owner;
        std::cout << "Owners: " << owner.use_count() << '\n';
        if (auto borrowed = observer.lock()) {
            std::cout << "Value: " << *borrowed << '\n';
        }
    }
    owner.reset();
    std::cout << std::boolalpha << "Expired: " << observer.expired() << '\n';
}
