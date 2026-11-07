#include <cstddef>
#include <print>
#include <utility>
#include <vector>

class Packet {
public:
    explicit Packet(std::vector<int> bytes) : bytes_(std::move(bytes)) {}
    Packet(const Packet&) = delete;
    Packet& operator=(const Packet&) = delete;
    Packet(Packet&&) noexcept = default;
    Packet& operator=(Packet&&) noexcept = default;
    [[nodiscard]] std::size_t size() const noexcept { return bytes_.size(); }
private:
    std::vector<int> bytes_;
};

int main() {
    Packet packet{{1, 2, 3, 4}};
    Packet delivered{std::move(packet)};
    std::println("Delivered bytes: {}", delivered.size());
    packet = Packet{{9}}; // Move 이후 재사용 가능
    std::println("Reused bytes: {}", packet.size());
}
