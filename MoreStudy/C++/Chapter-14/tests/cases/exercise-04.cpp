#include <iostream>
#include <stdexcept>
#include <vector>
#include CH14_SOURCE_PATH

void require(bool condition) { if (!condition) throw std::runtime_error("async results"); }
int main() {
    require(evaluate_in_parallel({2,4,6})==std::vector<long long>({4,16,36}));
    require(evaluate_in_parallel({})==std::vector<long long>{});
    require(evaluate_in_parallel({46341,0,1})==std::vector<long long>({2147488281LL,0,1}));
    bool invalid=false;
    try { (void)evaluate_in_parallel({2,-3,4}); }
    catch (const std::invalid_argument&) { invalid=true; }
    require(invalid);
    std::cout << "PASS\n";
}
