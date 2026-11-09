#include <iostream>
#include <list>
#include <numeric>
#include <vector>

int main() {
    const std::vector<int> contiguous{1, 2, 3, 4, 5};
    const std::list<int> linked{1, 2, 3, 4, 5};
    const int vector_total = std::accumulate(contiguous.begin(), contiguous.end(), 0);
    const int list_total = std::accumulate(linked.begin(), linked.end(), 0);
    std::cout << "Vector: " << vector_total << ", List: " << list_total << "\n";
}
