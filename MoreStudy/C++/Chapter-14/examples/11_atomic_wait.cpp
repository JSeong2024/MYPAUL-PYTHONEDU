#include <atomic>
#include <iostream>
#include <thread>

int main() {
    std::atomic<int> phase{0};
    int payload = 0;
    std::jthread consumer{[&] {
        phase.wait(0, std::memory_order_acquire);
        std::cout << "Payload: " << payload << '\n';
    }};
    payload = 73;
    phase.store(1, std::memory_order_release);
    phase.notify_one();
    consumer.join();
}
