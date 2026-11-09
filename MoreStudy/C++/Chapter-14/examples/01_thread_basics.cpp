#include <iostream>
#include <thread>

int main() {
    int result = 0;
    std::thread worker{[&result] { result = 21 * 2; }};
    worker.join(); // join 후에만 result를 읽는다.
    std::cout << "Result: " << result << '\n';
}
