#include <condition_variable>
#include <deque>
#include <iostream>
#include <mutex>
#include <optional>
#include <thread>

class ClosingQueue {
public:
    [[nodiscard]] bool push(int value) {
        {
            std::lock_guard lock{mutex_};
            if (closed_) return false;
            data_.push_back(value);
        }
        changed_.notify_one();
        return true;
    }
    [[nodiscard]] std::optional<int> pop() {
        std::unique_lock lock{mutex_};
        changed_.wait(lock, [&] { return closed_ || !data_.empty(); });
        if (data_.empty()) return std::nullopt;
        const int value = data_.front();
        data_.pop_front();
        return value;
    }
    void close() {
        {
            std::lock_guard lock{mutex_};
            closed_ = true;
        }
        changed_.notify_all();
    }
private:
    std::mutex mutex_;
    std::condition_variable changed_;
    std::deque<int> data_;
    bool closed_ = false;
};

#ifndef CH14_LIBRARY_ONLY
int main() {
    ClosingQueue queue;
    (void)queue.push(11);
    (void)queue.push(22);
    queue.close();
    const auto a = queue.pop();
    const auto b = queue.pop();
    const auto end = queue.pop();
    std::cout << "Values: " << a.value_or(-1) << ", " << b.value_or(-1)
              << ", Closed: " << std::boolalpha << !end.has_value() << '\n';
}
#endif
