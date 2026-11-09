#include "../common/socket.hpp"
#include <iostream>
int main() {
    lesson_net::Runtime runtime;
    auto socket = lesson_net::tcp_socket();
    lesson_net::set_timeout(socket, 100);
    std::cout << "Timeout configured (100 ms)\n";
    // A receive timeout is not an overall deadline for a multi-chunk transfer.
}
