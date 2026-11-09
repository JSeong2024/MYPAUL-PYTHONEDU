#include <condition_variable>
#include <iostream>
#include <mutex>
#include <stop_token>
#include <thread>
int main() {
    std::mutex mutex;
    std::condition_variable_any cv;
    bool work_ready = false;
    bool awakened = false;
    std::jthread worker([&](std::stop_token stop) {
        std::unique_lock lock{mutex};
        cv.wait(lock, stop, [&] { return work_ready; });
        awakened = stop.stop_requested();
    });
    worker.request_stop();
    worker.join();
    std::cout << "Stopped: " << std::boolalpha << awakened << '\n';
}
