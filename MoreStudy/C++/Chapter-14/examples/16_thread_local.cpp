#include <iostream>
#include <thread>

thread_local int local_sequence = 0;

int main() {
    int left = 0;
    int right = 0;
    std::jthread a{[&] { ++local_sequence; ++local_sequence; left = local_sequence; }};
    std::jthread b{[&] { ++local_sequence; right = local_sequence; }};
    a.join();
    b.join();
    std::cout << "Local counters: " << left << ", " << right << '\n';
}
