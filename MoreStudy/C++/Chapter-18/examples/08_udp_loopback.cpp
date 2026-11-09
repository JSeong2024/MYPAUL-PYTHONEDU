#include "../common/socket.hpp"
#include <iostream>
int main() {
    lesson_net::Runtime runtime;
    lesson_net::Socket receiver{::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)};
    lesson_net::Socket sender{::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)};
    if (!receiver.valid() || !sender.valid()) throw std::runtime_error("UDP socket failed");
    const auto addr = lesson_net::loopback_address(0);
    if (::bind(receiver.get(), reinterpret_cast<const sockaddr*>(&addr), sizeof(addr)) != 0)
        throw std::runtime_error("UDP bind failed");
    lesson_net::set_timeout(receiver, 1000);
    sockaddr_in bound{};
#ifdef _WIN32
    int len = sizeof(bound);
#else
    socklen_t len = sizeof(bound);
#endif
    if (::getsockname(receiver.get(), reinterpret_cast<sockaddr*>(&bound), &len) != 0)
        throw std::runtime_error("getsockname failed");
    constexpr char message[] = "sensor=42";
    if (::sendto(sender.get(), message, 9, 0,
                 reinterpret_cast<const sockaddr*>(&bound), sizeof(bound)) != 9)
        throw std::runtime_error("sendto failed");
    char buffer[32]{};
    const int received = ::recvfrom(receiver.get(), buffer, sizeof(buffer), 0, nullptr, nullptr);
    if (received != 9) throw std::runtime_error("UDP receive failed");
    std::cout << "Datagram: " << std::string(buffer, static_cast<std::size_t>(received)) << '\n';
}
