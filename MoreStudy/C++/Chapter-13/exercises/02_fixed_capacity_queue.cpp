#include <array>
#include <cstddef>
#include <print>

// TODO: FIFO 순서를 지키는 고정 용량 순환 큐 구현
// push: 공간이 없으면 false, pop: 비어 있으면 false
// Capacity는 1 이상으로 제한

template <typename T, std::size_t Capacity>
class FixedQueue {
public:
    [[nodiscard]] bool push(const T& value) {
        // TODO
        (void)value;
        return false;
    }
    [[nodiscard]] bool pop(T& output) {
        // TODO
        (void)output;
        return false;
    }
private:
    std::array<T, Capacity> data_{};
    std::size_t head_{};
    std::size_t size_{};
};

int main() {
    FixedQueue<int, 2> queue;
    int out{};
    const bool pushed = queue.push(10);
    const bool popped = queue.pop(out);
    std::println("Pushed: {}, popped: {}, value: {}", pushed, popped, out);
}
