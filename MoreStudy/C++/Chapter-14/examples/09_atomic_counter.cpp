#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

int main() {
    std::atomic<int> processed{0};
    std::vector<std::jthread> workers;
    for (int i = 0; i < 4; ++i) {
        workers.emplace_back([&] {
            for (int j = 0; j < 500; ++j)
                processed.fetch_add(1, std::memory_order_relaxed);
        });
    }
    for (auto& worker : workers) worker.join();
    std::cout << "Processed: " << processed.load() << '\n';
}
