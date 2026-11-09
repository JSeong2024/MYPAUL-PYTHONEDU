#include <condition_variable>
#include <iostream>
#include <mutex>
#include <stop_token>
#include <thread>

int main() {
    std::mutex mutex;
    std::condition_variable_any ready;
    bool has_work = false;
    bool stopped = false;
    std::jthread worker{[&](std::stop_token token) {
        std::unique_lock lock{mutex};
        const bool got_work = ready.wait(lock, token, [&] { return has_work; });
        stopped = !got_work;
    }};
    worker.request_stop(); // stop_token 지원 wait는 이 요청에 반응한다.
    worker.join();
    std::cout << "Stopped waiting: " << std::boolalpha << stopped << '\n';
}
