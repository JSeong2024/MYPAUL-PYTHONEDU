#include <array>
#include <cstddef>
#include <print>

template <typename T, std::size_t Capacity>
class FixedQueue {
    static_assert(Capacity > 0, "Capacity must be positive");
public:
    [[nodiscard]] bool push(const T& value) {
        if (size_ == Capacity) return false;
        data_[(head_ + size_) % Capacity] = value;
        ++size_;
        return true;
    }
    [[nodiscard]] bool pop(T& output) {
        if (size_ == 0) return false;
        output = data_[head_];
        head_ = (head_ + 1) % Capacity;
        --size_;
        return true;
    }
private:
    std::array<T, Capacity> data_{};
    std::size_t head_{};
    std::size_t size_{};
};

int main() {
    FixedQueue<int, 2> queue;
    int out{};
    std::println("Push 10: {}", queue.push(10));
    std::println("Push 20: {}", queue.push(20));
    std::println("Push 30: {}", queue.push(30));
    if (queue.pop(out)) std::println("Pop: {}", out);
    std::println("Push 30 again: {}", queue.push(30));
    if (queue.pop(out)) std::println("Pop: {}", out);
    if (queue.pop(out)) std::println("Pop: {}", out);
    std::println("Empty pop: {}", queue.pop(out));
}
