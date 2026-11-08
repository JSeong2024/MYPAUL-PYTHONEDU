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
        return payload_ ? payload_->size() : 0;
    }
    [[nodiscard]] int sum() const noexcept {
        if (!payload_) return 0;
        return std::accumulate(payload_->begin(), payload_->end(), 0);
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
