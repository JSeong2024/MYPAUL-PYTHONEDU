#include <cstdint>
#include <iostream>

struct PacketHeader {
    std::uint32_t message_id{};
    std::uint16_t payload_bytes{};
    bool encrypted{false};
};

int main() {
    const PacketHeader header{
        .message_id = 42,
        .payload_bytes = 128,
        .encrypted = true
    };
    std::cout << std::boolalpha;
    std::cout << "Packet " << header.message_id << ": "
              << header.payload_bytes << " bytes, encrypted: "
              << header.encrypted << '\n';
}
