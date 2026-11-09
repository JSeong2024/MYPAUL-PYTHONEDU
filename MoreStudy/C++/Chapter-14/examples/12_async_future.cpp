#include <future>
#include <iostream>

int main() {
    auto future = std::async(std::launch::async, [] { return 6 * 7; });
    std::cout << "Result: " << future.get() << '\n';
    // get()은 결과를 한 번 가져오며 예외도 호출자에게 전달한다.
}
