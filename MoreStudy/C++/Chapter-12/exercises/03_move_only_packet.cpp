#include <print>
#include <utility>
#include <vector>

class Packet {
public:
    explicit Packet(std::vector<int> bytes) : bytes_(std::move(bytes)) {}
    // TODO: 복사 금지, 이동 허용 (필요한 Special Member Function 선언)
    [[nodiscard]] std::size_t size() const noexcept { return bytes_.size(); }
private:
    std::vector<int> bytes_;
};

int main() {
    Packet packet{{1, 2, 3, 4}};
    // TODO: packet의 Ownership을 다른 Packet으로 이전
    std::println("Original size: {}", packet.size());
}
