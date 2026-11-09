#include "../common/socket.hpp"
#include <iostream>
int main() {
    lesson_net::Runtime runtime;
    std::uint16_t port = 0;
    auto listener = lesson_net::listen_loopback(port);
    auto moved = std::move(listener);
    std::cout << "Owner moved: " << std::boolalpha
              << (!listener.valid() && moved.valid()) << '\n';
}
