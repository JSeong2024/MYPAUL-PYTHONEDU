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
    [[nodiscard]] bool push(int value) {
        std::unique_lock lock{mutex_};
        space_.wait(lock, [&] { return closed_ || values_.size() < capacity_; });
        if (closed_) return false;
        values_.push_back(value);
        data_.notify_one();
        return true;
    }
    [[nodiscard]] std::optional<int> pop() {
        std::unique_lock lock{mutex_};
        data_.wait(lock, [&] { return closed_ || !values_.empty(); });
        if (values_.empty()) return std::nullopt;
        const int value = values_.front();
        values_.pop_front();
        space_.notify_one();
        return value;
    }
    void close() {
        std::lock_guard guard{mutex_};
        closed_ = true;
        space_.notify_all();
        data_.notify_all();
    }
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
    std::cout << queue.pop().value() << '\n'
              << std::boolalpha << !queue.pop() << '\n';
}
#endif
