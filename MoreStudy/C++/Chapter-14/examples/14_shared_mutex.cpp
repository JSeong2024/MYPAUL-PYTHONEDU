#include <iostream>
#include <mutex>
#include <shared_mutex>
#include <thread>
#include <vector>

class Registry {
public:
    void update(int value) {
        std::unique_lock lock{mutex_};
        value_ = value;
    }
    [[nodiscard]] int read() const {
        std::shared_lock lock{mutex_};
        return value_;
    }
private:
    mutable std::shared_mutex mutex_;
    int value_{};
};

int main() {
    Registry registry;
    registry.update(31);
    std::vector<int> readings(4);
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&, i] { readings[i] = registry.read(); });
    }
    for (auto& worker : workers) worker.join();
    std::cout << "Reads: " << readings[0] + readings[1]
              + readings[2] + readings[3] << '\n';
}
