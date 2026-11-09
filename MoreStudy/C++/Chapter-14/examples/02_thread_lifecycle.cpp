#include <iostream>
#include <thread>
#include <utility>

int main() {
    std::thread first{[] { /* 독립 작업 */ }};
    std::thread owner = std::move(first);
    std::cout << "Old joinable: " << std::boolalpha << first.joinable() << '\n';
    owner.join();
    std::cout << "Joined: " << !owner.joinable() << '\n';
}
