#include <barrier>
#include <iostream>
#include <latch>
#include <thread>

int main() {
    std::latch ready{2};
    std::barrier sync_point{2};
    int first = 0;
    int second = 0;
    std::jthread a{[&] {
        first = 10;
        ready.count_down();
        sync_point.arrive_and_wait();
        first += second;
    }};
    std::jthread b{[&] {
        second = 20;
        ready.count_down();
        sync_point.arrive_and_wait();
        // 이 단계에서는 공유 데이터를 추가로 쓰지 않는다.
    }};
    ready.wait(); // 준비가 끝났지만 각 스레드는 barrier에서 서로를 기다린다.
    a.join();
    b.join();
    std::cout << "Values: " << first << ", " << second << '\n';
}
