#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

int main() {
    int count = 0;
    std::mutex mutex;
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&] {
            for (int j = 0; j < 1000; ++j) {
                std::lock_guard lock{mutex};
                ++count;
            }
        });
    }
    for (auto& worker : workers) worker.join();
    std::cout << "Count: " << count << '\n';
}
