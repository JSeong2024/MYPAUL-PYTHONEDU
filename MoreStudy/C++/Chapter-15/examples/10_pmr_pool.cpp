#include <iostream>
#include <memory_resource>
#include <vector>

int main() {
    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> first{&pool};
    std::pmr::vector<int> second{&pool};
    first.push_back(7);
    second.push_back(9);
    std::cout << "Pool values: " << first.front() << ", " << second.front() << "\n";
    // Pool은 컨테이너보다 오래 살아야 함. 이 자원은 동시 사용에 안전하지 않음.
}
