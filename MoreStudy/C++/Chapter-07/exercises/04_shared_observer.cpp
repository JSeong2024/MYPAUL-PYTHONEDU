#include <iostream>
#include <memory>
#include <string>

int main() {
    auto owner = std::make_shared<std::string>("sensor-hub");
    // TODO: construct a weak_ptr, use lock() to print the active object,
    // release the last shared_ptr owner and print expired().
    std::cout << "Active: " << *owner << '\n';
    std::cout << std::boolalpha;
    std::cout << "Expired: " << false << '\n';
}
