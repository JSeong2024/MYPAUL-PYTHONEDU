#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

class Meter {
public:
    void add(int value) {
        std::lock_guard lock{mutex_};
        sum_ += value;
        ++count_; // sum_과 count_는 같은 잠금으로 보호한다.
    }
    void print() const {
        std::lock_guard lock{mutex_};
        std::cout << "Samples: " << count_ << ", Sum: " << sum_ << '\n';
    }
private:
    mutable std::mutex mutex_;
    int sum_{};
    int count_{};
};

int main() {
    Meter meter;
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) workers.emplace_back([&] { meter.add(5); });
    for (auto& worker : workers) worker.join();
    meter.print();
}
