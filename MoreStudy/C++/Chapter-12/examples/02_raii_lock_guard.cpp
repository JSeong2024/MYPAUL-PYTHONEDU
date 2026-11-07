#include <mutex>
#include <print>

class Counter {
public:
    void increment() {
        std::lock_guard<std::mutex> lock{mutex_};
        ++value_;
    }
    [[nodiscard]] int read() const {
        std::lock_guard<std::mutex> lock{mutex_};
        return value_;
    }
private:
    mutable std::mutex mutex_;
    int value_{0};
};

int main() {
    Counter counter;
    counter.increment();
    counter.increment();
    std::println("Count: {}", counter.read());
}
