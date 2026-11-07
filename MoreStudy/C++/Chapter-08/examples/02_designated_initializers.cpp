#include <cstdint>
#include <print>

struct PacketHeader {
    std::uint32_t message_id{};
    std::uint16_t payload_bytes{};
    bool encrypted{false};
};

int main() {
    const PacketHeader header{
        .message_id = 42,
        .payload_bytes = 128,
        .encrypted = true,
    };
    std::println("Packet {}: {} bytes, encrypted: {}",
                 header.message_id, header.payload_bytes, header.encrypted);
}
