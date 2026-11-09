#include <iostream>
#include <stop_token>
#include <thread>

int main() {
    bool observed_stop = false;
    std::jthread worker{[&](std::stop_token stop) {
        // 중단 토큰을 확인하는 최소 예제. 실무에서는 바쁜 대기 대신 대기 객체 사용.
        while (!stop.stop_requested()) std::this_thread::yield();
        observed_stop = true;
    }};
    worker.request_stop();
    worker.join();
    std::cout << "Stop observed: " << std::boolalpha << observed_stop << '\n';
    std::cout << "Joined: " << !worker.joinable() << '\n';
}
