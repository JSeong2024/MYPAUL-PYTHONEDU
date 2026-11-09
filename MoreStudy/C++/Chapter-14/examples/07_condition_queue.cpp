#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

int main() {
    std::mutex mutex;
    std::condition_variable ready;
    std::queue<int> queue;
    bool closed = false;
    int received = 0;
    std::jthread consumer{[&] {
        std::unique_lock lock{mutex};
        ready.wait(lock, [&] { return closed || !queue.empty(); });
        if (!queue.empty()) {
            received = queue.front();
            queue.pop();
        }
    }};
    {
        std::lock_guard lock{mutex};
        queue.push(42);
        closed = true;
    }
    ready.notify_one();
    consumer.join();
    std::cout << "Received: " << received << '\n';
}
