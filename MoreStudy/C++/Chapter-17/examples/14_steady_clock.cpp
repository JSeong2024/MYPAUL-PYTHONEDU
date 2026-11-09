#include <chrono>
#include <iostream>
#include <stdexcept>
int main() {
    const auto started=std::chrono::steady_clock::now();
    volatile int marker=0;
    (void)marker;
    const auto elapsed=std::chrono::steady_clock::now()-started;
    if(elapsed<decltype(elapsed)::zero())throw std::runtime_error("timer");
    std::cout << "Timer: monotonic\n"; // 실제 시간은 출력하지 않음
}
