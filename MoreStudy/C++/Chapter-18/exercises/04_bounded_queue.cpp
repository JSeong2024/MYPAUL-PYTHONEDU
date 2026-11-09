#include <condition_variable>
#include <cstddef>
#include <deque>
#include <mutex>
#include <optional>
#include <stdexcept>
class BoundedQueue {
public:
    explicit BoundedQueue(std::size_t capacity) : capacity_(capacity) {
        if (capacity == 0) throw std::invalid_argument("capacity must be positive");
    }
    // TODO: bounded blocking push. Closing rejects new pushes and wakes waiting writers.
    [[nodiscard]] bool push(int value) { (void)value; return false; }
    // TODO: wait for data or close. Drain buffered data even after close.
    [[nodiscard]] std::optional<int> pop() { return std::nullopt; }
    // TODO: notify all waiting producers and consumers.
    void close() {}
private:
    std::size_t capacity_;
    std::deque<int> values_;
    std::mutex mutex_;
    std::condition_variable data_;
    std::condition_variable space_;
    bool closed_{};
};
#ifndef CH18_LIBRARY_ONLY
#include <iostream>
int main() {
    BoundedQueue queue{2};
    (void)queue.push(7);
    queue.close();
    if (const auto value = queue.pop()) std::cout << *value << '\n';
}
#endif
