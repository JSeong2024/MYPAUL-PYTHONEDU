#include <climits>
#include <iostream>
#include <stdexcept>
#include <vector>
#include CH14_SOURCE_PATH

void require(bool condition) { if (!condition) throw std::runtime_error("parallel sum"); }
int main() {
    require(parallel_sum(std::vector<int>{1,2,3,4,5}, 3) == 15);
    require(parallel_sum(std::vector<int>{-50,0,100}, 8) == 50);
    require(parallel_sum(std::vector<int>{INT_MAX,INT_MAX,INT_MAX}, 2) == 3LL*INT_MAX);
    require(parallel_sum(std::vector<int>{}, 2) == 0);
    bool invalid = false;
    try { (void)parallel_sum(std::vector<int>{1}, 0); }
    catch (const std::invalid_argument&) { invalid = true; }
    require(invalid);
    std::vector<int> large(1000, 1);
    require(parallel_sum(large, 32) == 1000);
    std::cout << "PASS\n";
}
