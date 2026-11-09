#include <iostream>
#include <mutex>
#include <thread>
#include <vector>
class Counter {
public:
    void record() { std::lock_guard guard{mutex_}; ++count_; }
    [[nodiscard]] int value() const { std::lock_guard guard{mutex_}; return count_; }
private:
    mutable std::mutex mutex_;
    int count_{};
};
int main() {
    Counter counter;
    std::vector<std::jthread> workers;
    for (int t = 0; t < 4; ++t) {
        workers.emplace_back([&] { for (int i = 0; i < 250; ++i) counter.record(); });
    }
    workers.clear(); // joins all workers
    std::cout << "Processed: " << counter.value() << '\n';
}
