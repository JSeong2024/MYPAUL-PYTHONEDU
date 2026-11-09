#include "../common/socket.hpp"
#include <iostream>
int main() {
    const auto bytes = lesson_net::encode_frame("OK");
    std::cout << "Frame bytes: " << bytes.size() << '\n';
    std::cout << "Payload: " << bytes.substr(4) << '\n';
}
