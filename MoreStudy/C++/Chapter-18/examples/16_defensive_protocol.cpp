#include "../common/socket.hpp"
#include <iostream>
#include <string>
int main() {
    try {
        std::string oversize(lesson_net::max_payload + 1, 'a');
        (void)lesson_net::encode_frame(oversize);
    } catch (const std::length_error&) {
        std::cout << "Rejected: oversized payload\n";
    }
    const std::string data = lesson_net::encode_frame("PING");
    std::cout << "Accepted: " << data.size() << " bytes\n";
}
