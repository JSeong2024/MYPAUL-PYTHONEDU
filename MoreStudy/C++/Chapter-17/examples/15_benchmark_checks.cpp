#include <chrono>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
int main() {
    const std::vector values(1000,3);
    const auto begin=std::chrono::steady_clock::now();
    const int total=std::accumulate(values.begin(),values.end(),0);
    const auto elapsed=std::chrono::steady_clock::now()-begin;
    if(total!=3000 || elapsed<decltype(elapsed)::zero())throw std::runtime_error("benchmark");
    std::cout << "Result: 3000\n"; // 측정 시간은 환경에 따라 다름
}
