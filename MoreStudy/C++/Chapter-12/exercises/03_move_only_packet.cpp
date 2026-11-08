#include <cstddef>
#include <memory>
#include <numeric>
#include <utility>
#include <vector>
#ifndef CH12_LIBRARY_ONLY
#include <iostream>
#endif

class Packet {
public:
    explicit Packet(std::vector<int> values)
        : payload_(std::make_unique<std::vector<int>>(std::move(values))) {}
    Packet(const Packet&) = delete;
    Packet& operator=(const Packet&) = delete;
    Packet(Packet&&) noexcept = default;
    Packet& operator=(Packet&&) noexcept = default;

    [[nodiscard]] std::size_t size() const noexcept {
        // TODO: 소유한 payload가 없으면 0을 반환합니다.
        return 0;
    }
    [[nodiscard]] int sum() const noexcept {
        // TODO: payload가 있다면 합계를 계산합니다.
        return 0;
    }
private:
    std::unique_ptr<std::vector<int>> payload_;
};

#ifndef CH12_LIBRARY_ONLY
int main() {
    Packet input{{2, 3, 5}};
    Packet output{std::move(input)};
    std::cout << "Size: " << output.size() << ", Sum: " << output.sum() << '\n';
    std::cout << "Old size: " << input.size() << '\n';
}
#endif
