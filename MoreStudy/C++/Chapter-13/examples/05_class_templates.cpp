#include <array>
#include <cstddef>
#include <print>
#include <string>

template <typename T, std::size_t Capacity>
class FixedBuffer {
    static_assert(Capacity > 0, "Capacity must be positive");
public:
    [[nodiscard]] bool push(const T& value) {
        if (size_ == Capacity) return false;
        data_[size_++] = value;
        return true;
    }
    [[nodiscard]] std::size_t size() const noexcept { return size_; }
    [[nodiscard]] const T& at(std::size_t index) const { return data_.at(index); }
private:
    std::array<T, Capacity> data_{};
    std::size_t size_{};
};

int main() {
    FixedBuffer<std::string, 2> names;
    const bool first = names.push("front");
    const bool second = names.push("rear");
    const bool third = names.push("extra");
    std::println("Inserted: {} {} {}", first, second, third);
    std::println("Size: {}, First: {}", names.size(), names.at(0));
}
