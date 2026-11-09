#include <atomic>
#include <iostream>
#include <thread>

int main() {
    int payload = 0; // 원자 변수는 아니지만 release/acquire로 동기화한다.
    std::atomic<bool> ready{false};
    std::jthread producer{[&] {
        payload = 42;
        ready.store(true, std::memory_order_release);
    }};
    std::jthread consumer{[&] {
        while (!ready.load(std::memory_order_acquire)) std::this_thread::yield();
        std::cout << "Payload: " << payload << '\n';
    }};
    producer.join();
    consumer.join();
}
